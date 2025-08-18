import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import random
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

try:
    model = joblib.load('sentiment_model.pkl')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file 'sentiment_model.pkl' not found.")
    print("Please run the 'train_model.evaluate.py' script first to generate the model file.")
    model = None

class PredictionInput(BaseModel):
    text: str
    true_review: str

@app.get("/health")
def health_check():
    """
    Health Check Endpoint
    Simple endpoint to confirm that the API is running.
    """
    return {"status": "ok", "message": "API is running"}

@app.post("/predict")
def predict(input_data: PredictionInput):
    """
    Prediction Endpoint
    Takes a text input and returns the predicted sentiment of the movie review
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Cannot make predictions."
        )

    review_text = input_data.text
    prediction = model.predict([review_text])[0]

    #log prediction and other information
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "text": review_text,
        "predicted_sentiment": prediction,
        "true_sentiment": input_data.true_review
    }

    try:
        with open("../logs/prediction_logs.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except (fileNotFoundError, json.JSONDecodeError):
        print("File not found error")

    return {"sentiment": prediction, "true review": input_data.true_review}

@app.get("/example")
def training_example():
    """
    Training Example Endpoint
    Returns a random review from the original IMDB training dataset.
    This can be used to test the prediction endpoints
    """
    df = pd.read_csv('IMDB Dataset.csv')
    entry = random.randint(2,len(df))
    return {"review": df.iat[entry,0]}