import atexit
from typing import Optional
import pymongo


from app.utils.v1.configs import MONGO_URI
from app.utils.v1.LoggerSingleton import logger


class DatabaseSingleton:
    _instance: Optional['DatabaseSingleton'] = None
    _client = None
    _logs_integration_db = None
    _closed = False



    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance._initialize()
            atexit.register(cls._instance._safe_close)
        return cls._instance

    def _initialize(self):
        """Initialize MongoDB connection and collections"""


        self._client = pymongo.MongoClient(MONGO_URI)
        db = self._client.cuida_saludDB
        self._logs_integration_ms_db = db.logs_integration_ms
        self._closed = False
        logger.info(f"Database connection established: {MONGO_URI.split('@')[1]}")

    @property
    def logs_integration_ms(self):
        """Get logs_integration collection"""
        return self._logs_integration_ms_db


    def _safe_close(self):
        """Safe close method that handles shutdown gracefully"""
        if not self._closed and self._client:
            try:
                self._client.close()
                self._closed = True
                logger.info("Database connection closed safely")
            except Exception:
                # Ignorar errores durante el shutdown
                pass


    def close(self):
        """Close MongoDB connection"""
        self._client['_safe_close']

    def __del__(self):
        """Destructor to ensure connection is closed"""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
