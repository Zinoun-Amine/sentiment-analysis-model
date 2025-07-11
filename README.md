# TikTok Reviews Sentiment Analysis

This project analyzes sentiment in TikTok reviews using Python for the backend and provides a web interface for visualization.

## Project Structure

```
.
├── backend/
│   ├── app.py              # Flask API server
│   ├── preprocess.py       # Text preprocessing module
│   └── sentiment_analyzer.py # Sentiment analysis module
├── data/
│   └── reviews.csv         # Your dataset
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place your TikTok reviews dataset in the `data` folder as `reviews.csv`. The CSV should have a column named 'review' containing the text to analyze.

## Running the Backend

Start the Flask server:
```bash
cd backend
python app.py
```

The server will run on `http://localhost:5000`

## API Endpoints

1. Analyze single text:
   - POST `/api/analyze`
   - Body: `{"text": "your text here"}`

2. Analyze batch of reviews:
   - POST `/api/analyze-batch`
   - Form data: Upload a CSV file with a 'review' column

## Next Steps

1. Set up the frontend application
2. Create visualization components
3. Implement real-time analysis features
4. Add more advanced sentiment analysis features 