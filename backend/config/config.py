import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', True)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    ROOT_DIR = os.path.dirname(BASE_DIR)
    DATA_DIR = os.path.join(ROOT_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    SAVED_MODELS_DIR = os.path.join(BASE_DIR, 'saved_models')
    RAW_REVIEWS_FILE = os.path.join(RAW_DATA_DIR, 'tiktok_google_play_reviews.csv')
    PROCESSED_REVIEWS_FILE = os.path.join(PROCESSED_DATA_DIR, 'processed_tiktok_reviews.csv')
    MODEL_FILE_PATH = os.path.join(SAVED_MODELS_DIR, 'sentiment_model.joblib')
    VECTORIZER_FILE_PATH = os.path.join(SAVED_MODELS_DIR, 'tfidf_vectorizer.joblib')

    MAX_SEQUENCE_LENGTH = 128
    BATCH_SIZE = 32
    EPOCHS = 10
    LEARNING_RATE = 2e-5
    
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    
    MAX_COMMENTS_PER_VIDEO = 100
    
    SENTIMENT_CLASSES = ['Negative', 'Neutral', 'Positive']
    SENTIMENT_LABELS = { 'Negative': 0, 'Neutral': 1, 'Positive': 2 }