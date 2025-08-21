from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_positive():
    response = client.post("/predict", json={
        "text": "Fun plot with entertaining twists.",
        "true_review": "positive"
    })
    assert response.status_code == 200
    assert "predicted_sentiment" in response.json()

def test_predict_negative():
    response = client.post("/predict", json={
        "text": "Terrible waste of time.",
        "true_review": "negative"
    })
    assert response.status_code == 200
    assert "predicted_sentiment" in response.json()

def test_missing_field():
    response = client.post("/predict", json={"text": "Missing sentiment."})
    assert response.status_code == 422