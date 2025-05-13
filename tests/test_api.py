import pytest
from fastapi.testclient import TestClient

from app.api.app import app

client = TestClient(app)

def test_api_health():
    """Test that the API is running and responding to requests."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"

def test_api_documentation():
    """Test that the API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
