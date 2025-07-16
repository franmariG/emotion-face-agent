# Se importan librerías necesarias para enviar peticiones HTTP y manejar JSON
import requests
import json


# Función que envía el prompt al modelo Ollama (Gemma 3) y devuelve la respuesta completa como string
def ask_ollama(prompt: str) -> str:
    # URL del endpoint local de la API de Ollama
    url = "http://localhost:11434/api/chat"
    # Cuerpo de la solicitud: se define el modelo y el mensaje del usuario
    payload = {
        "model": "gemma3",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    # Se hace la solicitud POST a la API de Ollama, habilitando el stream para recibir la respuesta por partes
    response = requests.post(url, json=payload, stream=True)
    # Variable para acumular toda la respuesta del modelo IA
    full_response = ""

    # Se itera cada línea recibida en la respuesta (streaming)
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8')) # Se convierte cada línea JSON a diccionario
            if "message" in data and "content" in data["message"]:
                # Si existe contenido en la respuesta, se va acumulando
                full_response += data["message"]["content"]

    # Se devuelve la respuesta completa limpia, o un mensaje de error si no hubo respuesta
    return full_response.strip() if full_response else "No response from Ollama."
