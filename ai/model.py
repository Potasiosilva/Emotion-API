import os
import subprocess
from joblib import load
import logging
from preprocessing.preprocessing import Preprocessor

class EmotionModel:
    def __init__(self):
        self.model, self.vectorizer = self.load_model()

    def load_model(self):
        if not os.path.exists('model.joblib') or not os.path.exists('vectorizer.joblib'):
            logging.info("Los archivos del modelo no existen. Ejecutando save_model.py para entrenar y guardar el modelo.")
            subprocess.run(["python", "save_model.py"])
        model = load('model.joblib')
        vectorizer = load('vectorizer.joblib')
        return model, vectorizer

    def predict_emotion(self, text):
        try:
            preprocessor = Preprocessor()
            text_preprocessed = preprocessor.preprocess_text(text)
            text_tfidf = self.vectorizer.transform([text_preprocessed])
            emotion = self.model.predict(text_tfidf)
            return emotion[0]
        except Exception as e:
            logging.error(f"Error en predict_emotion: {e}")
            return "Error"

emotion_model = EmotionModel()
