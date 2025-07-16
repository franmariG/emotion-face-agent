# Garc-IA: Reconocimiento Facial de Identidad y Emoción para la Personalización de Agente Conversacional con IA Generativa
Proyecto de asistente conversacional personalizado que adapta su comportamiento según la identidad y la emoción detectada en imágenes faciales, utilizando clasificación CNN y generación de lenguaje mediante Ollama Gemma 3.

## Descripción del Proyecto
Garc-IA es un sistema conversacional capaz de identificar a la persona y su estado emocional a partir de imágenes faciales. Posteriormente, ajusta su tono de respuesta y comportamiento según esta información. Está pensado como una demostración de cómo integrar visión por computadora y modelos generativos para mejorar la personalización en la interacción humano-computadora.

## Principales características:
* Reconoce identidad y emoción (2 personas, 7 emociones) mediante CNN.
* Adapta tono, estilo de lenguaje y contenido de las respuestas a la persona y su emoción.
* Generación de texto mediante Ollama Gemma 3.
* Conversación mantenida mediante contexto almacenado.
* Interfaz web minimalista para interacción usuario-IA.


## Tecnologías utilizadas

| Área | Herramienta             | 
|--------|------------------|
| Backend | Python 3.11, FastAPI     | 
| Frontend  | HTML, CSS, Vanilla JS     | 
| Clasificación de imágenes | TensorFlow / Keras CNN | 
| Generación de respuestas  | Ollama Gemma 3 | 
| Base de datos | SQLite (contexto y conversación) |
| Librerías extra | Pillow, HTTPX, Requests |

## Estructura del Proyecto
```
app/
 ├─ models/
 │   └─ ollama_agent.py      # Comunicación con Ollama Gemma 3
 ├─ services/
 │   ├─ image_service.py     # CNN para identidad + emoción
 │   ├─ db_service.py        # SQLite para contexto e historial
 │   └─ chat_service.py      # Lógica de prompts y contexto
 ├─ static/
 │   └─ styles.css           # Estilos para la interfaz
 ├─ templates/
 │   └─ index.html           # Interfaz web
 └─ main.py                  # FastAPI principal
database/
 └─ chat_history.db          # SQLite DB
saved_models/
 └─ modelo_cnn.keras         # Modelo CNN entrenado
```

 
## Instrucciones para Ejecutar Localmente

### 1. Clonar repositorio
```bash
git clone https://github.com/franmariG/emotion-face-agent.git
cd emotion-face-agent
```
### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Ejecutar Ollama localmente
Asegúrate de tener Ollama instalado y corriendo el modelo Gemma 3.

```bash
ollama run gemma3
```
### 5. Ejecutar la API
```bash
uvicorn app.main:app --reload
Accede a http://localhost:8000 para usar la aplicación.
```

## Ejemplo de Uso
1. Carga una imagen facial.
2. El sistema reconoce quién eres y tu emoción actual.
3. El agente ajusta sus respuestas acorde a tu identidad y tu estado emocional.
4. Puedes seguir enviando mensajes para mantener una conversación contextualizada.

## ¿Cómo funciona?
* Clasificación de imagen (Identidad + Emoción)
CNN entrenada sobre un dataset personalizado. Devuelve Franmari_alegre, Mariannis_cansado, etc.

* Contexto Conversacional
Guarda quién es el usuario, su emoción y el historial.

* Generación de Respuesta
Prompt dinámico construido según persona y emoción.

 Se envía a Ollama (gemma3) para generar la respuesta natural.

## Notas Importantes
- La emoción detectada no se altera, el agente respeta siempre el resultado del análisis.
- La primera respuesta tras enviar una imagen menciona explícitamente que se ha recibido y reconoce la emoción.
- El historial extenso podría afectar la fluidez de la respuesta.


## Créditos
Proyecto desarrollado por 

**Franmari Garcia** Usuario de Github: franmariG 

**Mariannis Garcia** Usuario de Github: angeles1107

IA de lenguaje: Ollama - Gemma 3

Modelo CNN propio entrenado sobre dataset personalizado.

