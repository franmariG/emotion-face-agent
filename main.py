# Librerías de FastAPI para rutas, archivos, formularios y plantillas
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# Se importan servicios propios del proyecto
from app.services.image_service import predict_image # CNN para predecir persona y emoción
from app.services.db_service import save_context, get_context, save_chat # Gestión BD
from app.services.chat_service import chat_with_agent # Generación del prompt
import httpx # Cliente HTTP asíncrono para Ollama
import json # Procesar respuestas en streaming de Ollama

# Configuración inicial de FastAPI
app = FastAPI()

# Se monta la carpeta de recursos estáticos (CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Se configura plantillas Jinja para renderizar HTML dinámico
templates = Jinja2Templates(directory="app/templates")

# RUTA PRINCIPAL
# Renderiza la interfaz gráfica principal (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# RUTA PARA PROCESAR LA IMAGEN
# Recibe la imagen, predice usuario + emoción, y guarda contexto
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    prediction = predict_image(contents) # CNN devuelve algo como: "Franmari_alegre"
    persona, emocion = prediction.split("_")

    # Se guarda persona, emoción y que hay imagen nueva sin mencionar
    save_context(persona, emocion)

    return {"prediction": prediction} # Devuelve la predicción


# Función auxiliar para enviar mensajes a Ollama y recibir respuesta en streaming 
async def stream_ollama(prompt):
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://localhost:11434/api/chat",
            json={
                "model": "gemma3",
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            },
            timeout=None
        ) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    yield line + "\n"

# RUTA PARA MANEJAR EL CHAT
# Recibe mensaje del usuario, genera prompt completo, llama a Ollama y guarda la respuesta IA
@app.post("/chat/")
async def chat(user_message: str = Form(...)):
    context = get_context()
    persona = context["persona"]

    # Genera el prompt ajustado según persona, emoción e historial
    full_prompt = chat_with_agent(user_message)

    # Función asíncrona para procesar la respuesta por streaming
    async def stream_and_save():
        collected_response = ""
        async for line in stream_ollama(full_prompt):
            if line.strip():
                try:
                    # Procesa cada línea para acumular la respuesta IA completa
                    json_data = json.loads(line)
                    content = json_data.get("message", {}).get("content", "")
                    collected_response += content
                    yield line + "\n"
                except Exception as e:
                    print(f"Error processing streamed line: {line}")
        # Guarda la respuesta completa cuando termina
        save_chat(user="Agente IA", message=collected_response.strip(), persona=persona)
    
    # Devuelve la respuesta al cliente en tiempo real
    return StreamingResponse(stream_and_save(), media_type="text/plain")