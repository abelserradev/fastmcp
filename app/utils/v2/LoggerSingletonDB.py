import sys
import os
from datetime import datetime
from loguru import logger
from app.utils.v1.MongoDBHandler import setup_mongodb_handler


class LoggerSingletonDB:
    _instance = None

    def __new__(cls,app_name="IntegracionMS"):
        if cls._instance is None:
            logger.remove()
            logs_dir = "logs"
            try:
                if not os.path.exists(logs_dir):
                    os.makedirs(logs_dir, exist_ok=True)
            except Exception as e:
                logger.warning(f"File logging disabled (cannot create logs dir '{logs_dir}'): {e}")
                logs_dir = None

            logger.add(
                sys.stdout,
                colorize=True,
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                       f"<blue>{app_name}</blue> | "
                       "{level} | "
                       "<level>{message}</level>",
            )

            # --- Handler para archivos (con rotación diaria) ---
            if logs_dir is not None:
                log_filename = os.path.join(
                    logs_dir,
                    f"{datetime.now().strftime('%Y-%m-%d')}.log"
                )
                try:
                    logger.add(
                        log_filename,
                        rotation="12:00",  # Create new file at midnight
                        retention="30 days",  # Keep logs for 30 days
                        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                               f"{app_name} | "
                               "{level} | "
                               "{message}",
                    )
                except Exception as e:
                    logger.warning(f"File logging disabled (failed to open '{log_filename}'): {e}")
            try:
                mongodb_handler = setup_mongodb_handler()
                logger.add(
                    mongodb_handler,
                    level="INFO",  # Define el nivel mínimo de logs para MongoDB
                    serialize=True,  # Esta es la clave para enviar el log completo como JSON
                )
            except Exception as e:
                logger.warning(f"MongoDB logging disabled (setup failed): {e}")
            cls._instance = logger

        return cls._instance

logger = LoggerSingletonDB(app_name="IntegracionMS")

