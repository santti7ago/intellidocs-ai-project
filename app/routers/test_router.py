# app/routers/test_router.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping_test():
    """
    Una ruta de prueba simple para verificar si el enrutamiento funciona.
    """
    return {"message": "pong from test router!"}