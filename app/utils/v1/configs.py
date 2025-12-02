import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.v1.LoggerSingleton import logger

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# Detectar si estamos en modo MCP
IS_MCP_MODE = os.environ.get("MCP_SERVER_MODE") == "true"

# Define a Settings class that inherits from BaseSettings
class Settings(BaseSettings):
    # Define the attributes of the Settings class
    # Si estamos en modo MCP, hacer todas las variables opcionales excepto las necesarias
    API_KEY_AUTH: str | None = None
    SM_PRIMARY_KEY: str | None = None
    SM_SECONDARY_KEY: str | None = None
    SM_ENDPOINT: str | None = None
    USER: str | None = None
    APPLICATION: str | None = None
    SUBSCRIPTION_KEY: str | None = None
    ENV: str | None = None
    ALLOWED_HOST: str | None = None
    SUMA_ASEGURADA: int | None = None
    SM_PRIMARY_PASARELA_KEY: str | None = None
    SM_ENDPOINT_PASARELA_MS: str | None = None
    SM_PRIMARY_SUSCRIPTION_KEY: str | None = None
    SM_ENDPOINT_SUSCRIPCION: str | None = None
    MID: str | None = None
    MOCKUP: bool | None = None
    SM_ENDPOINT_NOTIFICACION_PAGO: str | None = None
    SM_NOTIFICACION_PAGO_KEY: str | None = None
    MONGO_URI: str | None = None
    URL_ANULAR_POLIZA: str | None = None
    API_KEY_ANULAR_POLIZA: str | None = None

    # Campos opcionales para MCP (con valores por defecto)
    JWT_SECRET_KEY: str | None = None
    BACKEND_BASE_URL: str | None = None
    API_TOKEN_MCP: str | None = None

    # Load the settings from the .env file
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )



@lru_cache()
def get_settings() -> Settings:
    """
    This function returns an instance of the Settings class.
    It uses the lru_cache decorator to cache the result,
    so that subsequent calls do not have to re-instantiate the Settings class.
    """
    return Settings()


# Get the settings
settings = get_settings()

def get_mcp_api_token() -> str:
    from app.mcp.exceptions import MCPErrorAuth
    settings = get_settings()

    if not settings.API_TOKEN_MCP:
        raise MCPErrorAuth(
            "API_TOKEN_MCP no está configurado. "
            "Por favor, configure API_TOKEN_MCP como variable de entorno."
        )
    return settings.API_TOKEN_MCP


def get_mcp_local_token() -> str:
    """
    Obtiene el token local para autenticación del servidor MCP.
    
    Returns:
        str: El token local configurado en MCP_LOCAL_TOKEN
        
    Raises:
        MCPErrorAuth: Si el token no está configurado
    """
    from app.mcp.exceptions import MCPErrorAuth
    settings = get_settings()
    
    # MCP_LOCAL_TOKEN no está en Settings, así que lo obtenemos directamente del entorno
    mcp_local_token = os.environ.get("MCP_LOCAL_TOKEN")
    
    if not mcp_local_token:
        raise MCPErrorAuth(
            "MCP_LOCAL_TOKEN no está configurado. "
            "Por favor, configure MCP_LOCAL_TOKEN como variable de entorno."
        )
    return mcp_local_token


# Assign the settings to variables (solo si no estamos en modo MCP o si están definidas)
if not IS_MCP_MODE:
    API_KEY_AUTH = settings.API_KEY_AUTH or ""
    SM_PRIMARY_KEY = settings.SM_PRIMARY_KEY or ""
    SM_SECONDARY_KEY = settings.SM_SECONDARY_KEY or ""
    SM_ENDPOINT = settings.SM_ENDPOINT or ""
    USER = settings.USER or ""
    APPLICATION = settings.APPLICATION or ""
    SUBSCRIPTION_KEY = settings.SUBSCRIPTION_KEY or ""
    ENV = settings.ENV or ""
    ALLOWED_HOST = settings.ALLOWED_HOST or ""
    SUMA_ASEGURADA = settings.SUMA_ASEGURADA or 0
    SM_PRIMARY_PASARELA_KEY = settings.SM_PRIMARY_PASARELA_KEY or ""
    SM_ENDPOINT_PASARELA_MS = settings.SM_ENDPOINT_PASARELA_MS or ""
    MID = settings.MID or ""
    MOCKUP = settings.MOCKUP or False
    SM_PRIMARY_SUSCRIPTION_KEY = settings.SM_PRIMARY_SUSCRIPTION_KEY or ""
    SM_ENDPOINT_SUSCRIPCION = settings.SM_ENDPOINT_SUSCRIPCION or ""
    SM_ENDPOINT_NOTIFICACION_PAGO = settings.SM_ENDPOINT_NOTIFICACION_PAGO or ""
    SM_NOTIFICACION_PAGO_KEY = settings.SM_NOTIFICACION_PAGO_KEY or ""
    MONGO_URI = settings.MONGO_URI or ""
    URL_ANULAR_POLIZA = settings.URL_ANULAR_POLIZA or ""
    API_KEY_ANULAR_POLIZA = settings.API_KEY_ANULAR_POLIZA or ""
else:
    # En modo MCP, solo definir las variables que realmente se usan
    API_KEY_AUTH = settings.API_KEY_AUTH or ""


def get_valid_api_keys() -> list[str]:
    valid_keys = []
    if settings.API_KEY_AUTH:
        valid_keys.append(settings.API_KEY_AUTH)
    
    # Agregar el token MCP si está configurado (para que el MCP pueda autenticarse)
    if settings.API_TOKEN_MCP:
        valid_keys.append(settings.API_TOKEN_MCP)
    
    return valid_keys

# Log that the settings have been loaded
if not IS_MCP_MODE:
    logger.info("Settings loaded")
