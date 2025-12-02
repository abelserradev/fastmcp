import pytest
from unittest.mock import Mock, AsyncMock
from app.mcp.auth import JWTAuthHandler
from app.mcp.client import BackendClient


@pytest.fixture
def jwt_handler():
    """Fixture para el manejador JWT."""
    return JWTAuthHandler(secret_key="test_secret_key")


@pytest.fixture
def mock_backend_client():
    """Fixture para un cliente backend mockeado."""
    client = Mock(spec=BackendClient)
    client.post = AsyncMock()
    return client


@pytest.fixture
def valid_token(jwt_handler):
    """Fixture para generar un token JWT válido."""
    return jwt_handler.encode_token({"user_id": "test_user"})


@pytest.fixture
def invalid_token():
    """Fixture para un token inválido."""
    return "invalid_token_string"