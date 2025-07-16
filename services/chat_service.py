# Se importan funciones para manipular base de datos y contexto actual
from app.services.db_service import get_context, save_chat, get_chat_history, mark_image_as_mentioned

# PROMPT PARA FRANMARI 
# Instrucciones específicas para el estilo y tono del agente al hablar con Franmari
PROMPT_FRANMARI = """
Eres un asistente conversacional reconocedor de emociones cercano, amable y natural con Franmari. A ella le gustan las charlas relajadas, la tecnología, la programación, y un toque ligero de humor. Puedes usar emojis ocasionalmente para dar calidez, pero no exageres.
Si Franmari está triste, anímala con empatía sincera. Si está alegre, comparte su alegría con naturalidad. Si está cansada, responde con calma y comprensión.
No seas repetitivo ni demasiado efusivo. Habla con expresiones cotidianas, como si la conocieras de tiempo atrás. Siempre dirige tus respuestas mencionando su nombre.
IMPORTANTE: Si te he indicado que la emoción es "ira", nunca la cambies por "triste" u otra. Respeta exactamente la emoción indicada. Lo mismo pasa con las demas emociones
Solo saluda (Hola, buenas tardes, etc) si Franmari te saluda en su ultimo mensaje, si no lo hace solo menciona su nombre de manera natural.
"""

# PROMPT PARA MARIANNIS
# Instrucciones específicas para el estilo y tono del agente al hablar con Mariannis
PROMPT_MARIANNIS = """
Eres un asistente conversacional reconocedor de emociones que habla con Mariannis. Ella disfruta de conversaciones sobre música, cine, libros y arte. Siempre debes mantener un tono claro, respetuoso y amable. No uses emojis.
IMPORTANTE:
Si has recibido recientemente una imagen de Mariannis, tu primera respuesta DEBE mencionar explícitamente que viste su imagen (por ejemplo: "En la foto que me enviaste...") y debes mencionar la emoción detectada (por ejemplo: "pareces alegre"). Esto es obligatorio y solo debe hacerse una vez por cada imagen.
Nunca cambies la emoción indicada por otra. Si dice "ira" debes decir "ira" no "tristeza". Si dice que "esta riendo", debes decir que "esta riendo". Lo mismo pasa con las demas emociones.
Si Mariannis está cansada o pensativa, responde con calma y pocas palabras. Si está triste, ofrece comprensión sincera. Si está alegre, acompaña su estado hablando de sus intereses.
No uses diminutivos, bromas innecesarias, ni lenguaje técnico. Sé claro, directo y amable.
Incluye siempre su nombre, Mariannis, al menos una vez en cada respuesta.
Solo saluda (Hola, buenas tardes, etc.) si Mariannis te ha saludado en su último mensaje. Si no lo ha hecho, responde directamente usando su nombre, sin saludos.
ATENCIÓN: Aunque este sea un tono serio y claro, es obligatorio cumplir todas las instrucciones indicadas sobre mencionar la imagen y la emoción al recibir una foto. No debes ignorarlo por ninguna razón. Si no cumples esta instrucción se considerará que tu respuesta es inválida.
"""


# Generador del prompt completo para enviar a Ollama
def build_prompt(persona, emocion, user_message, imagen_mencionada=False, user_greeted=False):
    # Selecciona el prompt base según la persona identificada
    if persona == "Franmari":
        base = PROMPT_FRANMARI
        ejemplo = """
        Ejemplo:
        Franmari: Hola, ¿cómo estás?
        IA: ¡Hola Franmari! Qué gusto saludarte. 😊

        Franmari: Me siento cansada.
        IA: Entiendo Franmari, es normal. Cuida tu energía.

        Franmari: ¿Sabías que hoy aprendí algo nuevo de Python?
        IA: Qué interesante, Franmari. Me alegra que sigas aprendiendo.
        """
    else:
        base = PROMPT_MARIANNIS
        ejemplo = """
        Ejemplo:
        Mariannis: Buenas tardes.
        IA: Buenas tardes, Mariannis. ¿Estás disfrutando tu día?

        Mariannis: Estoy un poco cansada.
        IA: Lo entiendo, Mariannis. A veces un buen libro o una canción tranquila ayudan a desconectar.

        Mariannis: Hoy estuve leyendo sobre cine independiente.
        IA: Qué interesante, Mariannis. Ese tipo de cine suele tener historias muy auténticas. ¿Viste algo que te haya gustado últimamente?

        Mariannis: Sí, una película francesa bastante buena.
        IA: Me alegra que hayas encontrado algo que te gustara, Mariannis. Siempre es un placer descubrir cine diferente.
        """

    # Si se recibió imagen y aún no se mencionó, se refuerza la instrucción de mencionarla en la respuesta
    emocion_msg = ""
    if emocion != "Desconocida" and not imagen_mencionada:
        emocion_msg = (
        f"\n\n***ATENCIÓN:*** Has recibido una imagen que muestra que {persona} está {emocion}."
        f"\nEn tu primera respuesta tras recibir esa imagen debes SIEMPRE mencionar literalmente:"
        f" que has visto su foto (por ejemplo: 'en la foto que me enviaste...') y mencionar la emoción detectada (por ejemplo: 'te noto {emocion}')."
        f"\nNo ignores esta instrucción. Si ya lo hiciste antes, no lo repitas.\n"
    )
        
    # Indica si se debe saludar o no, según si el usuario ha saludado primero
    saludo_instr = ""
    if user_greeted:
        saludo_instr = f" Puedes saludar a {persona} de forma amable."
    else:
        saludo_instr = f" No saludes a {persona} a menos que te haya saludado primero."

    # Define tono extra para adaptar mejor la respuesta según la emoción
    tono = ""
    if "triste" in emocion:
        tono = " El usuario se siente triste, sé empático, muestra comprensión sincera y cuidado en tus palabras."
    elif "alegre" in emocion:
        tono = " El usuario se siente alegre, sé entusiasta, demuestra alegría por su estado."
    elif "riendo" in emocion:
        tono = " El usuario esta riendo, sé divertido, responde con humor ligero y buena actitud."
    elif "sorprendido" in emocion:
        tono = " El usuario esta sorprendido, sé animado y curioso, comparte la emoción."
    elif "cansado" in emocion:
        tono = " El usuario se siente cansado, sé breve, directo, habla con calma y evita dar demasiada información."
    elif "pensativo" in emocion:
        tono = " El usuario se siente pensativo, sé reflexivo, invita a la introspección y aporta ideas tranquilas."
    elif "ira" in emocion:
        tono = " El usuario siente iracundo o molesto, sé calmado, reconoce su ira, ofrece soluciones o escucha activamente para desescalar la situación."

    # Historial de chat para mantener coherencia en la conversación
    chat_history = get_chat_history(persona)
    history_text = ""
    for user, message in chat_history:
        if user == "Agente IA":
            history_text += f"IA: {message}\n"
        else:
            history_text += f"{persona}: {message}\n"
            
    # Construcción del prompt final para enviar al modelo
    prompt = (
    f"{base}\n"
    f"{emocion_msg}{tono}\n"
    f"{saludo_instr}\n\n"
    f"***IMPORTANTE:*** En cada respuesta debes mencionar SIEMPRE el nombre de {persona} al menos una vez.\n"
    f"RECUERDA: Si has recibido una imagen, en tu primera respuesta debes decir explícitamente que viste la foto y la emoción detectada.\n"
    f"No ignores estas instrucciones.\n\n"
    f"{ejemplo}\n"
    "Esta es la conversación reciente:\n"
    f"{history_text}"
    f"{persona}: {user_message}\n"
    "IA:"
)
    return prompt

# Función que detecta si el usuario ha saludado para decidir si el agente puede devolver saludo
def detect_saludo(user_message: str) -> bool:
    saludos = ["hola", "buenas", "buenos días", "buenos dias", "buenas tardes", "buenas noches", "saludos", "hey"]
    mensaje = user_message.lower()
    return any(saludo in mensaje for saludo in saludos)

# Función principal para generar el prompt listo para Ollama
def chat_with_agent(user_message: str):
    # Recupera la información actual de la persona, emoción y si ya se mencionó la imagen
    context = get_context()
    persona = context["persona"]
    emocion = context["emocion"]
    imagen_mencionada = context.get("imagen_mencionada", False)

    # Detecta si el usuario ha saludado
    user_greeted = detect_saludo(user_message)

    # Genera el prompt completo a partir de la información obtenida
    full_prompt = build_prompt(persona, emocion, user_message, imagen_mencionada, user_greeted)

    # Si aún no se había mencionado la imagen, se marca que ya se hizo
    if not imagen_mencionada:
        mark_image_as_mentioned()

    # Guarda el mensaje del usuario en la base de datos
    save_chat(user=persona, message=user_message, persona=persona)

    # Devuelve el prompt completo
    return full_prompt
