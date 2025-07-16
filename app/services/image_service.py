# Librerías para manejo de imágenes, arrays y el modelo CNN
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from keras.utils import img_to_array
from keras.models import load_model

# Ruta al modelo CNN previamente entrenado y guardado
MODEL_PATH = 'saved_models/modelo_cnn.keras'
model = load_model(MODEL_PATH) # Se carga el modelo Keras (.keras)

# Lista de clases posibles que el modelo puede predecir (nombre_persona_emoción)
CLASS_NAMES = [
    'Franmari_alegre', 'Franmari_cansado', 'Franmari_ira', 'Franmari_pensativo',
    'Franmari_riendo', 'Franmari_sorprendido', 'Franmari_triste',
    'Mariannis_alegre', 'Mariannis_cansado', 'Mariannis_ira', 'Mariannis_pensativo',
    'Mariannis_riendo', 'Mariannis_sorprendido', 'Mariannis_triste'
]

# Función para realizar la predicción de la emoción a partir de una imagen
def predict_image(image_bytes):
    
    # Se convierten los bytes recibidos en una imagen RGB
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Se redimensiona la imagen al tamaño esperado por la CNN
    img = img.resize((150, 150))
    # Se convierte la imagen a array numérico compatible con Keras
    img_array = img_to_array(img)

    # Se añade una dimensión para indicar que es un único lote de imágenes
    img_array = np.expand_dims(img_array, axis=0)

    # Se ejecuta la predicción con el modelo CNN
    prediction = model.predict(img_array)
    
    # Se muestra en consola las probabilidades para fines de depuración
    print("Probabilidades:", prediction)

    # Se toma la clase con mayor probabilidad como predicción final
    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    
    # Se devuelve la clase predicha (ejemplo: 'Franmari_triste')
    return predicted_class
