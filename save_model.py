import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from joblib import dump

class ModelTrainer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = SVC()
        
    def train_and_save_model(self):
        df = pd.read_csv('eng_dataset.csv')
        X = df['content']
        y = df['sentiment']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        self.model.fit(X_train_tfidf, y_train)
        accuracy = self.model.score(X_test_tfidf, y_test)
        print(f'Precisión del modelo: {accuracy}')
        
        # Guardar el modelo y el vectorizador
        dump(self.model, 'model.joblib')
        dump(self.vectorizer, 'vectorizer.joblib')

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_and_save_model()
