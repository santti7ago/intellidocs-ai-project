# app/services/gemini_service.py

import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def get_gemini_analysis(text: str) -> dict | None:
    """
    Envía el texto extraído a la API de Gemini para su análisis.
    Devuelve un diccionario con el análisis o None si falla.
    """
    prompt = f"""
    Analiza el siguiente texto y devuelve EXCLUSIVAMENTE un objeto JSON válido con la siguiente estructura:
    - "title": Un título adecuado y conciso para el documento.
    - "summary": Un resumen ejecutivo de 3 o 4 frases clave.
    - "keywords": una lista de 5 a 7 palabras clave importantes.

    NO incluyas "
json" ni "
" en la respuesta. La respuesta debe ser solo el JSON.

    Texto del documento:
    ---
    {text[:8000]}
    ---
    """
    try:
        model = genai.GenerativeModel('models/gemini-pro-latest')
        response = await model.generate_content_async(prompt)
        result_text = response.text.strip()

        # Extraer el bloque JSON de la respuesta para mayor robustez
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if not json_match:
            print(f"Error: No se encontró JSON en la respuesta de Gemini. Respuesta: {result_text}")
            return None
            
        json_string = json_match.group(0)
        return json.loads(json_string)

    except Exception as e:
        print(f"Error durante la llamada o procesamiento de Gemini: {e}")
        return None