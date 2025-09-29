# app/models/user.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from .document import PyObjectId

class UserModel(BaseModel):
    """Modelo base para un usuario en la base de datos."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            PyObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }

class UserInCreate(BaseModel):
    """Modelo para la creación de un nuevo usuario."""
    email: EmailStr = Field(...)
    password: str = Field(...)

class UserInResponse(BaseModel):
    """Modelo para las respuestas de la API, NUNCA incluye la contraseña."""
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }