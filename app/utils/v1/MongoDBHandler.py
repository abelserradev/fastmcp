import sys
import datetime
from app.utils.v1.database import DatabaseSingleton
from app.utils.v1.LoggerSingleton import logger


class MongoDBHandler:
    """Handles interaction with MongoDB database.

    Provides methods to connect, read, write, and perform other operations on a MongoDB
    database. Suitable for applications requiring persistent storage and retrieval of
    structured data.

    Attributes:
        uri (str): MongoDB connection URI.
        database_name (str): Name of the database to connect to.
    """
    def __init__(self):
        self.db_instance = DatabaseSingleton()

    def _serialize_record(self, record):
        """Convert record to MongoDB-compatible format."""
        serialized = {}

        for key, value in record.items():
            serialized[key] = self._serialize_value(value)

        return serialized

    def _serialize_value(self, value):
        """Helper method to serialize individual values."""
        # Handle datetime types
        if isinstance(value, datetime.timedelta):
            return value.total_seconds()
        elif isinstance(value, datetime.datetime):
            return value

        # Handle Loguru record types specifically by their class name
        elif value.__class__.__name__ in ('RecordFile', 'RecordLevel', 'RecordProcess', 'RecordThread'):
            # Convert Loguru record objects to dictionaries
            if hasattr(value, 'name') and hasattr(value, 'path'):
                # RecordFile
                return {'name': value.name, 'path': value.path}
            elif hasattr(value, 'name') and hasattr(value, 'no'):
                # RecordLevel
                return {'name': value.name, 'no': value.no, 'icon': getattr(value, 'icon', '')}
            elif hasattr(value, 'id') and hasattr(value, 'name'):
                # RecordProcess or RecordThread
                return {'id': value.id, 'name': value.name}
            else:
                # Fallback for other Loguru objects
                return str(value)

        # Handle standard named tuples
        elif hasattr(value, '_asdict'):
            return value._asdict()

        # Handle dictionaries recursively
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}

        # Handle lists and tuples
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value]

        # Handle primitive types and everything else
        else:
            # Test if the value is JSON serializable
            try:
                import json
                json.dumps(value)
                return value
            except (TypeError, ValueError):
                # If not serializable, convert to string
                return str(value)

    def __call__(self, msg):
        record = msg.record

        try:
            # Serialize the record to make it MongoDB-compatible
            serialized_record = self._serialize_record(record)
            self.db_instance.logs_integration_ms.insert_one(serialized_record)
        except Exception as e:
            # Use print instead of logger to avoid deadlock
            print(f"Error inserting log into MongoDB: {e}", file=sys.stderr)


def setup_mongodb_handler():
    handler = MongoDBHandler()
    logger.info("Configurando handler de MongoDB para reutilizar la conexión Singleton...")
    return handler