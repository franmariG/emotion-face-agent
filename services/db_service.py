import sqlite3
import os

# Ruta donde se guarda la base de datos SQLite
DB_PATH = "app/database/chat_history.db"

# Si la carpeta no existe, se crea
if not os.path.exists("app/database"):
    os.makedirs("app/database")
    
#  CREACIÓN DE LAS TABLAS SI NO EXISTEN

# Tabla chat: almacena todos los mensajes del usuario y de la IA, indicando a quién pertenece cada conversación
conn = sqlite3.connect(DB_PATH)
conn.execute('''CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    message TEXT,
    persona TEXT
)''')

# Tabla context: guarda solo el contexto actual (persona, emoción y si ya se mencionó la imagen)
conn.execute('''CREATE TABLE IF NOT EXISTS context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona TEXT,
    emocion TEXT,
    imagen_mencionada BOOLEAN DEFAULT 0
)''')
conn.close()

# FUNCIONES PARA MANIPULAR LA BASE DE DATOS

# Guarda cada mensaje en la tabla chat, incluyendo la persona asociada
def save_chat(user, message, persona="Desconocido"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat (user, message, persona) VALUES (?, ?, ?)", (user, message, persona))
    conn.commit()
    conn.close()

# Guarda el contexto actual: persona, emoción y que aún no se ha mencionado la imagen
def save_context(persona, emocion):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM context")
    cursor.execute("INSERT INTO context (persona, emocion, imagen_mencionada) VALUES (?, ?, ?)", (persona, emocion, False))
    conn.commit()
    conn.close()


# Obtiene el contexto actual para saber quién está interactuando, su emoción, y si ya se mencionó su imagen
def get_context():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT persona, emocion, imagen_mencionada FROM context ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"persona": row[0], "emocion": row[1], "imagen_mencionada": bool(row[2])}
    else:
        return {"persona": "Desconocido", "emocion": "Desconocida", "imagen_mencionada": False}

# Recupera todo el historial de mensajes asociados a una persona específica (Franmari o Mariannis)
def get_chat_history(persona):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user, message FROM chat WHERE persona = ? ORDER BY id", (persona,))
    history = cursor.fetchall()
    conn.close()
    return history

# Marca que ya se mencionó la última imagen enviada, para no repetir en las respuestas futuras
def mark_image_as_mentioned():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE context SET imagen_mencionada = 1")
    conn.commit()
    conn.close()
