
import os
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from config.config import Config

class SentimentClassifier:
    def __init__(self):
        self.model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=20000, min_df=5, max_df=0.7)
        self.is_trained = False

    def _clean_text(self, text):
        # Convertir en minuscules
        text = str(text).lower()
        # Supprimer les caractères spéciaux et la ponctuation
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Supprimer les espaces supplémentaires
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def train(self, train_texts, train_labels):
        print("Vectorizing training data...")
        train_vectors = self.vectorizer.fit_transform(train_texts)
        
        print("Training the Logistic Regression model...")
        self.model.fit(train_vectors, train_labels)
        self.is_trained = True
        print("✅ Model training complete.")

    def predict(self, texts):
        if not self.is_trained and not self.load_model():
             raise RuntimeError("Model is not trained or loaded. Cannot predict.")
        
        cleaned_texts = [self._clean_text(text) for text in texts]
        vectors = self.vectorizer.transform(cleaned_texts)
        return self.model.predict(vectors)

    def save_model(self):
        os.makedirs(Config.SAVED_MODELS_DIR, exist_ok=True)
        joblib.dump(self.model, Config.MODEL_FILE_PATH)
        joblib.dump(self.vectorizer, Config.VECTORIZER_FILE_PATH)
        print(f"Model and vectorizer saved successfully to {Config.SAVED_MODELS_DIR}")

    def load_model(self):
        model_exists = os.path.exists(Config.MODEL_FILE_PATH)
        vectorizer_exists = os.path.exists(Config.VECTORIZER_FILE_PATH)

        if model_exists and vectorizer_exists:
            self.model = joblib.load(Config.MODEL_FILE_PATH)
            self.vectorizer = joblib.load(Config.VECTORIZER_FILE_PATH)
            self.is_trained = True
            print("Pre-trained model and vectorizer loaded.")
            return True
        return False