import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from ai.model import emotion_model

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)

# Definir la ruta para predecir la emoción
@app.route('/predict_emotion', methods=['POST'])
def predict_emotion_api():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No se proporcionó texto para predecir.'}), 400
        
        text = data['text']
        
        if not isinstance(text, str) or not text.strip():
            return jsonify({'error': 'El texto proporcionado no es válido.'}), 400
        
        emotion = emotion_model.predict_emotion(text)
        return jsonify({'emotion': emotion})
    
    except Exception as e:
        logging.error(f"Error al procesar la solicitud: {e}")
        return jsonify({'error': 'Ocurrió un error interno en el servidor.'}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Error al iniciar la aplicación: {e}")
