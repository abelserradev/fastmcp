import os
import sys
import pytest

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

os.environ.setdefault("ENV", "test")
os.environ.setdefault("MOCKUP", "true")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/test_db_fake")

mock_mongodb_handler = MagicMock()
mock_mongodb_handler.__call__ = MagicMock(return_value=None)

mock_setup_handler = patch(
    'app.utils.v1.MongoDBHandler.setup_mongodb_handler',
    return_value=mock_mongodb_handler
)
mock_setup_handler.start()

original_new = None

def mock_database_new(cls):
    """Mock de DatabaseSingleton.__new__ que evita inicialización real."""
    if cls._instance is None:
        instance = MagicMock()
        instance._client = MagicMock()
        instance._closed = False
        instance._logs_integration_ms_db = MagicMock()
        instance.logs_integration_ms = MagicMock()
        instance.logs_integration_ms.insert_one = MagicMock()
        instance._safe_close = MagicMock()  # Mock del método de cierre
        instance.close = MagicMock()
        cls._instance = instance
    return cls._instance

mock_db_new = patch('app.utils.v1.database.DatabaseSingleton.__new__', side_effect=mock_database_new)
mock_db_new.start()

mock_db_init = patch('app.utils.v1.database.DatabaseSingleton._initialize', return_value=None)
mock_db_init.start()

try:
    from app.api.app import app
except Exception as e:
    print(f"Error importando app: {e}")
    raise




@pytest.fixture(scope="session", autouse=True)
def clean_despues_tests():
    yield
    from loguru import logger
    try:
        logger.remove()
        logger.add(sys.stdout, level="ERROR", format="{message}")
    except Exception:
        pass

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def api_key():
    return "test_api_key"


@pytest.fixture
def headers(api_key):
    return {
        "X-API-Key": api_key
    }

