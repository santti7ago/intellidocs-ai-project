# app/main.py

from fastapi import FastAPI
# 1. Importamos el middleware de CORS
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documents, auth

app = FastAPI(
    title="IntelliDocs AI API",
    description="API para la gestión inteligente de documentos con IA.",
    version="1.0.0",
)

# 2. Añadimos el middleware de CORS a la aplicación
#    Esto le dice al backend que acepte peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Incluir los routers
app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint de bienvenida para verificar que la API está en línea."""
    return {"message": "Welcome to IntelliDocs AI API"}