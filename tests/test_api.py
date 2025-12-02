import pytest
from fastapi.testclient import TestClient
from app.api.app import app

pytest_plugins = ["tests.configtest"]

# client = TestClient(app)

# def test_api_health():
#     """Test that the API is running and responding to requests."""
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert "status" in response.json()
#     assert response.json()["status"] == "ok"

# def test_api_documentation():
#     """Test that the API documentation is accessible."""
#     response = client.get("/docs")
#     assert response.status_code == 200
#     assert "text/html" in response.headers["content-type"]


@pytest.mark.e2e
class Testendpoints:
    def test_endpoints(self, client: TestClient):
        expected_status = 200
        expected_response = {"status": "ok"}
        response = client.get("/health")

        assert response.status_code == expected_status
        assert "status" in response.json()
        assert response.json() == expected_response

    def test_documentacion(self, client: TestClient):
        expected_status = 200
        expected_content_type = "text/html"

        response = client.get("/docs")
        assert response.status_code == expected_status
        assert expected_content_type in response.headers["content-type"]
