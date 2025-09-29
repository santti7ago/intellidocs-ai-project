# app/routers/auth.py

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone

from app.models.user import UserInCreate, UserInResponse
from app.database import user_collection
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserInResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserInCreate):
    """
    Registra un nuevo usuario en la base de datos.
    - Verifica si el email ya existe.
    - Hashea la contraseña antes de guardarla.
    """
    existing_user = await user_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )

    hashed_password = get_password_hash(user_data.password)
    
    new_user_data = {
        "email": user_data.email,
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }

    result = await user_collection.insert_one(new_user_data)
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    
    # --- CAMBIO IMPORTANTE AQUÍ ---
    # Creamos manualmente el campo 'id' a partir del '_id' de MongoDB
    # para que coincida con nuestro modelo de respuesta Pydantic.
    created_user["id"] = str(created_user["_id"])
    # -----------------------------

    return UserInResponse(**created_user)


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica al usuario y devuelve un token de acceso JWT.
    """
    user = await user_collection.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user["email"]}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}