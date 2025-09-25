import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_chat():
    response = client.post("/chat", json={"query": "What is the policy on vacation?", "history": []})
    assert response.status_code == 200
    assert "answer" in response.json()