# check_models.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar la variable de entorno
load_dotenv()

try:
    # Configurar la API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    print("--- Modelos de IA compatibles encontrados para tu API Key ---")
    
    # Listar todos los modelos y filtrar los que sirven para generar contenido
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")

    print("\nCopia uno de estos nombres (ej. 'models/gemini-1.0-pro') y pégalo en tu archivo gemini_service.py")

except Exception as e:
    print(f"!!! Ocurrió un error: {e} !!!")
    print("Verifica que tu GOOGLE_API_KEY en el archivo .env sea correcta.")