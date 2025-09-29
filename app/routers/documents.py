# app/routers/documents.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from bson import ObjectId
import fitz  # PyMuPDF

from app.models.document import DocumentResponse, UpdateDocumentModel, DocumentModel
from app.models.user import UserModel
from app.database import document_collection
from app.security import get_current_user
from app.services.gemini_service import get_gemini_analysis

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"]
)

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Sube, analiza y guarda un nuevo documento. Endpoint protegido.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Solo se aceptan archivos PDF.")

    try:
        pdf_bytes = await file.read()
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            extracted_text = "".join(page.get_text() for page in doc)

        if not extracted_text.strip():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "El PDF no contiene texto.")

        analysis_result = await get_gemini_analysis(extracted_text)
        if not analysis_result:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "El análisis de IA falló.")
        
        document_data = DocumentModel(
            filename=file.filename,
            analysis=analysis_result,
            owner_id=str(current_user.id)
        )
        
        result = await document_collection.insert_one(document_data.model_dump())
        created_document = await document_collection.find_one({"_id": result.inserted_id})
        
        return DocumentResponse(**created_document)

    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error al procesar el archivo: {e}")


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(current_user: UserModel = Depends(get_current_user)):
    """
    Lista todos los documentos que pertenecen al usuario autenticado.
    """
    documents = await document_collection.find({"owner_id": str(current_user.id)}).to_list(100)
    return [DocumentResponse(**doc) for doc in documents]


@router.get("/{id}", response_model=DocumentResponse)
async def get_document_by_id(id: str, current_user: UserModel = Depends(get_current_user)):
    """
    Obtiene un documento específico por su ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "ID de documento inválido.")
    
    doc = await document_collection.find_one({"_id": ObjectId(id)})
    
    if doc and doc["owner_id"] == str(current_user.id):
        return DocumentResponse(**doc)
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Documento no encontrado.")


@router.put("/{id}", response_model=DocumentResponse)
async def update_document_by_id(id: str, doc_update: UpdateDocumentModel, current_user: UserModel = Depends(get_current_user)):
    """
    Actualiza los metadatos de un documento.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "ID de documento inválido.")
    
    doc = await document_collection.find_one({"_id": ObjectId(id)})
    
    if not doc or doc["owner_id"] != str(current_user.id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Documento no encontrado.")

    update_data = doc_update.model_dump(exclude_unset=True)
    
    # El modelo de actualización puede contener campos de nivel superior o dentro de 'analysis'
    update_query = {}
    if "title" in update_data:
        update_query["analysis.title"] = update_data["title"]
    if "summary" in update_data:
        update_query["analysis.summary"] = update_data["summary"]
    if "keywords" in update_data:
        update_query["analysis.keywords"] = update_data["keywords"]

    if not update_query:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No hay datos para actualizar.")

    await document_collection.update_one({"_id": ObjectId(id)}, {"$set": update_query})
    
    updated_doc = await document_collection.find_one({"_id": ObjectId(id)})
    return DocumentResponse(**updated_doc)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_by_id(id: str, current_user: UserModel = Depends(get_current_user)):
    """
    Elimina un documento por su ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "ID de documento inválido.")
    
    doc = await document_collection.find_one({"_id": ObjectId(id)})
    
    if not doc or doc["owner_id"] != str(current_user.id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Documento no encontrado.")
        
    delete_result = await document_collection.delete_one({"_id": ObjectId(id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Documento no encontrado para eliminar.")
    
    return