import sys
import os
from datetime import datetime
from loguru import logger

class LoggerSingleton:
    _instance = None

    def __new__(cls, app_name="IntegracionMS"):
        if cls._instance is None:
            # Remove any existing handlers
            logger.remove()

            # Create logs directory if it doesn't exist (best-effort)
            logs_dir = "logs"
            try:
                if not os.path.exists(logs_dir):
                    os.makedirs(logs_dir, exist_ok=True)
            except Exception as e:
                # If we cannot create the logs directory (e.g., read-only FS or permissions),
                # we will gracefully degrade to console-only logging.
                logger.warning(f"File logging disabled (cannot create logs dir '{logs_dir}'): {e}")
                logs_dir = None

            # Generate log filename with date
            log_filename = None
            if logs_dir:
                log_filename = os.path.join(
                    logs_dir,
                    f"{datetime.now().strftime('%Y-%m-%d')}.log"
                )

            # Detectar si estamos ejecutando como servidor MCP (usando stdio para JSON)
            # Los servidores MCP usan stdout para JSON, así que debemos usar stderr para logs
            # y deshabilitar colores para evitar códigos ANSI que interfieren con JSON
            import inspect
            is_mcp_server = False
            
            # Verificar variable de entorno
            if os.environ.get("MCP_SERVER_MODE") == "true":
                is_mcp_server = True
            # Verificar si el módulo que lo está llamando es parte del módulo MCP
            else:
                try:
                    frame = inspect.currentframe()
                    while frame:
                        module_name = frame.f_globals.get('__name__', '')
                        if 'mcp' in module_name.lower() and 'server' in module_name.lower():
                            is_mcp_server = True
                            break
                        frame = frame.f_back
                except Exception:
                    pass
            
            # Verificación adicional: si se ejecuta como módulo app.mcp.server
            if not is_mcp_server:
                all_args = ' '.join(sys.argv).lower()
                if 'app.mcp.server' in all_args or '-m app.mcp.server' in all_args:
                    is_mcp_server = True
                elif any('mcp' in arg.lower() and 'server' in arg.lower() for arg in sys.argv):
                    is_mcp_server = True
            
            # Add handler for console output (real-time logs)
            # Si es servidor MCP, usar stderr para no interferir con la comunicación JSON en stdout
            # y deshabilitar colores completamente
            if is_mcp_server:
                # En modo MCP: usar stderr, sin colores, formato simple
                logger.add(
                    sys.stderr,
                    colorize=False,
                    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                           f"{app_name} | "
                           "{level} | "
                           "{message}",
                )
            else:
                # Modo normal: usar stdout, con colores
                logger.add(
                    sys.stdout,
                    colorize=True,
                    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                           f"<blue>{app_name}</blue> | "
                           "{level} | "
                           "<level>{message}</level>",
                )

            # Add handler for file output (best-effort, skip if not possible)
            if log_filename is not None:
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

            cls._instance = logger

        return cls._instance

# Create a logger instance
logger = LoggerSingleton(app_name="IntegracionMS")  # noqa: F811
