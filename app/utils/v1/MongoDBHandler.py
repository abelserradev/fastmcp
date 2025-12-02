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

        if 'time' in record:
            serialized['time'] = self._serialize_value(record['time'])

        if 'level' in record:
            level = record['level']
            serialized['level'] = {
                'name': level.name,
                'no': level.no,
            }
            if hasattr(level, 'icon'):
                serialized['level']['icon'] = level.icon

        if 'message' in record:
            serialized['message'] = str(record['message'])


        if 'name' in record:
            serialized['name'] = record['name']

        if 'file' in record and record['file']:
            file_obj = record['file']
            serialized['file'] = {
                'name': file_obj.name if hasattr(file_obj, 'name') else None,
                'path': file_obj.path if hasattr(file_obj, 'path') else None,
                }
                
        if 'module' in record:
            serialized['module'] = record['module']

        if 'function' in record:
            serialized['function'] = record['function']

        if 'line' in record:
            serialized['line'] = record['line']


        if 'process' in record and record['process']:
            proc = record['process']
            serialized['process'] = {'id': proc.id if hasattr(proc, 'id') else None,
            'name': proc.name if hasattr(proc, 'name') else None}


        if 'thread' in record and record['thread']:
            thread = record['thread']
            serialized['thread'] = {
                'id': thread.id if hasattr(thread, 'id') else None,
                'name': thread.name if hasattr(thread, 'name') else None,
            }

        if 'exception' in record and record['exception']:
            serialized['exception'] = self._serialize_value(record['exception'])

        if 'extra' in record and record['extra']:
            serialized['extra'] = self._serialize_value(record['extra'])

        if 'elapsed' in record:
            serialized['elapsed'] = self._serialize_value(record['elapsed'])

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