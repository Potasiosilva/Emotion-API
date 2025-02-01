import nltk
from nltk.corpus import stopwords
import string
import logging
from googletrans import Translator
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Descargar los stop words de nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Inicializar el traductor de googletrans
translator = Translator()

class Preprocessor:
    def __init__(self):
        self.stop_words = stop_words
        self.translator = translator

    def preprocess_text(self, text, retries=5, wait=10):
        attempt = 0
        while attempt < retries:
            try:
                translated_text = self.translator.translate(text, dest='en').text
                text = translated_text.lower()
                text = text.translate(str.maketrans('', '', string.punctuation))
                text = ' '.join([word for word in text.split() if word not in self.stop_words])
                return text
            except Exception as e:
                logging.error(f"Error en preprocess_text: {e}")
                time.sleep(wait)
                attempt += 1
        return text
