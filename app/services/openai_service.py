# app/services/openai_service.py

import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Configurar el cliente de OpenAI con la API Key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_ai_analysis(text: str) -> dict:
    """
    Envía el texto extraído a la API de OpenAI para su análisis.
    """
    # Prompt de ingeniería: La instrucción que le damos a la IA
    prompt = f"""
    Analiza el siguiente texto extraído de un documento y devuelve un objeto JSON con los siguientes campos:
    - "title": Un título adecuado y conciso para el documento.
    - "summary": Un resumen ejecutivo de 3 o 4 frases clave.
    - "keywords": una lista de 5 a 7 palabras clave o conceptos importantes.

    Asegúrate de que la respuesta sea únicamente el objeto JSON, sin texto adicional antes o después.

    Texto del documento:
    ---
    {text[:4000]}
    ---
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis y resumen de documentos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Le pedimos a la IA que sea más precisa y menos creativa
        )

        # Extraer el contenido de la respuesta y convertirlo a un diccionario
        result_text = response.choices[0].message.content
        return json.loads(result_text)

    except Exception as e:
        print(f"Error al conectar con OpenAI: {e}")
        return None