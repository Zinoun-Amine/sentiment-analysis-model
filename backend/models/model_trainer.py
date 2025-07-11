
import os
import joblib
from sklearn.model_selection import train_test_split
from models.model_evaluator import display_evaluation_metrics
from config.config import Config
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from lightgbm import LGBMClassifier


def train_and_evaluate(texts, labels):

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    print(f"Original data split: {len(X_train)} training, {len(X_test)} testing.")

    
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(ngram_range=(1, 2), max_features=20000, min_df=5, max_df=0.7)),
        ('sampler', RandomUnderSampler(random_state=42)),
        ('classifier', LGBMClassifier(random_state=42, class_weight='balanced', n_jobs=-1))
    ])
    
    print("\nTraining the final LightGBM pipeline...")
    pipeline.fit(X_train, y_train)

    print("\nEvaluating model on the original (imbalanced) test set...")
    predictions = pipeline.predict(X_test)
    display_evaluation_metrics(y_test, predictions, model_name="Final Model: LightGBM with Undersampling")
    
    os.makedirs(Config.SAVED_MODELS_DIR, exist_ok=True)
    pipeline_path = os.path.join(Config.SAVED_MODELS_DIR, 'sentiment_pipeline.joblib')
    joblib.dump(pipeline, pipeline_path)
    print(f"\n Final pipeline saved successfully to: {pipeline_path}")
