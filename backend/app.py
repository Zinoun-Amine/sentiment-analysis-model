import os
import sys
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.config import Config

app = Flask(__name__)
CORS(app) 
sentiment_pipeline = None
try:
    pipeline_path = os.path.join(Config.SAVED_MODELS_DIR, 'sentiment_pipeline.joblib')
    sentiment_pipeline = joblib.load(pipeline_path)
    print(f"Sentiment analysis pipeline loaded successfully from: {pipeline_path}")
except Exception as e:
    print(f"ERROR: Could not load the sentiment pipeline. Details: {e}")
    print("Please make sure you have run the training script successfully.")

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    if sentiment_pipeline is None:
        return jsonify({'error': 'Model is not available. Please check the server logs.'}), 503
    
    data = request.get_json()
    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({'error': 'No text provided'}), 400
    
    text_to_analyze = data['text']

    try:
        prediction = sentiment_pipeline.predict([text_to_analyze])[0]
        return jsonify({
            'text': text_to_analyze,
            'sentiment': str(prediction) 
        })
    
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500
@app.route('/')
def index():
    return "Sentiment Analysis API is running!"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)