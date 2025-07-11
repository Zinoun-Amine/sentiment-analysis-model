# backend/train_model.py
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from models.model_trainer import train_and_evaluate

def run_preprocessing():
    print("--- 1. Preprocessing Data ---")
    if not os.path.exists(Config.RAW_REVIEWS_FILE):
        print(f"❌ ABORT: Raw data not found at {Config.RAW_REVIEWS_FILE}")
        return False
    
    df = pd.read_csv(Config.RAW_REVIEWS_FILE)
    df.dropna(subset=['content', 'score'], inplace=True)
    
    def assign_sentiment(score):
        if score >= 4: return 'Positive'
        elif score <= 2: return 'Negative'
        else: return 'Neutral'

    df['sentiment'] = df['score'].apply(assign_sentiment)
    df.rename(columns={'content': 'text'}, inplace=True)
    df_clean = df.loc[df['text'].str.len() >= 10, ['text', 'sentiment']]
    
    os.makedirs(Config.PROCESSED_DATA_DIR, exist_ok=True)
    df_clean.to_csv(Config.PROCESSED_REVIEWS_FILE, index=False)
    print(f"✅ Saved {len(df_clean)} cleaned reviews to {Config.PROCESSED_REVIEWS_FILE}")
    return True

def start_training_pipeline():
    """Main function to run the full training pipeline."""
    if not os.path.exists(Config.PROCESSED_REVIEWS_FILE):
        print("Processed data file not found. Running preprocessing first.")
        if not run_preprocessing():
            return
    
    print("\n--- 2. Loading Processed Data ---")
    df = pd.read_csv(Config.PROCESSED_REVIEWS_FILE)
    print(f"Loaded {len(df)} reviews for training.")
    print(f"Sentiment distribution:\n{df['sentiment'].value_counts(normalize=True).round(2)}")
    
    # Trigger the training and evaluation workflow
    train_and_evaluate(df['text'].tolist(), df['sentiment'].tolist())

if __name__ == "__main__":
    start_training_pipeline()