# app/database.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Configuramos la conexión con un timeout para evitar que se congele
client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    # Comprobar la conexión al iniciar
    client.admin.command('ping')
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")


db = client.intellidocs_db
document_collection = db.get_collection("documents")
user_collection = db.get_collection("users")