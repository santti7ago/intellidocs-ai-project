# app/models/document.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Permite convertir el _id de MongoDB a un string
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not isinstance(v, str):
            # Asumimos que es un ObjectId si no es un string
            return str(v)
        return v

class DocumentAnalysis(BaseModel):
    """Modelo para el análisis generado por la IA."""
    title: str
    summary: str
    keywords: List[str]

class DocumentModel(BaseModel):
    """Modelo base para un documento en la base de datos."""
    filename: str
    analysis: DocumentAnalysis
    owner_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DocumentResponse(DocumentModel):
    """Modelo para las respuestas de la API, incluye el ID."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            PyObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }

class UpdateDocumentModel(BaseModel):
    """Modelo para actualizar un documento. Todos los campos son opcionales."""
    title: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None