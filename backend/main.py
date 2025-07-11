# backend/main.py (Version 9.0 - FINAL, CORRECT STRUCTURE)

import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
from collections import Counter
from config.config import Config
class ReviewRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    sentiment: Literal['Negative', 'Neutral', 'Positive']

class SampleAnalysisResponse(BaseModel):
    total_comments: int; positive_count: int; negative_count: int; neutral_count: int
    positive_percentage: float; negative_percentage: float; neutral_percentage: float

app = FastAPI(title="TikTok Review Sentiment Analysis API", version="9.0")
origins = ["http://localhost:4200"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

sentiment_pipeline = None
df_reviews = None
try:
    pipeline_path = os.path.join(Config.SAVED_MODELS_DIR, 'sentiment_pipeline.joblib')
    sentiment_pipeline = joblib.load(pipeline_path)

    df_reviews = pd.read_csv(Config.PROCESSED_REVIEWS_FILE)
    df_reviews.dropna(subset=['text'], inplace=True)

    print("Final Pipeline and review dataset loaded successfully.")
except Exception as e:
    print(f"ERREUR AU DÉMARRAGE: Could not load model or data. Details: {e}")

@app.post("/predict", response_model=PredictionResponse)
def predict_sentiment(request: ReviewRequest):
    if not sentiment_pipeline:
        raise HTTPException(status_code=503, detail="Model pipeline is not loaded.")
    predicted_sentiment = sentiment_pipeline.predict([request.text])[0]
    return {"sentiment": predicted_sentiment}

@app.get("/analyze-sample", response_model=SampleAnalysisResponse)
def analyze_sample():
    if df_reviews is None or sentiment_pipeline is None:
        raise HTTPException(status_code=503, detail="Dataset or model pipeline is not available.")
    
    sample_size = min(100, len(df_reviews))
    sample_df = df_reviews.sample(n=sample_size, random_state=42)
    comments = sample_df['text'].tolist()
    sentiments = sentiment_pipeline.predict(comments)
    sentiment_counts = Counter(sentiments)
    total_comments = len(sentiments)
    positive_count = sentiment_counts.get('Positive', 0)
    negative_count = sentiment_counts.get('Negative', 0)
    neutral_count = sentiment_counts.get('Neutral', 0)
    
    response_data = {
        "total_comments": total_comments, "positive_count": positive_count,
        "negative_count": negative_count, "neutral_count": neutral_count,
        "positive_percentage": round((positive_count / total_comments) * 100, 2) if total_comments > 0 else 0,
        "negative_percentage": round((negative_count / total_comments) * 100, 2) if total_comments > 0 else 0,
        "neutral_percentage": round((neutral_count / total_comments) * 100, 2) if total_comments > 0 else 0
    }
    return response_data