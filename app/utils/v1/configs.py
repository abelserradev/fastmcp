from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.v1.LoggerSingleton import logger

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# Define a Settings class that inherits from BaseSettings
class Settings(BaseSettings):
    # Define the attributes of the Settings class
    API_KEY_AUTH: str
    SM_PRIMARY_KEY: str
    SM_SECONDARY_KEY: str
    SM_ENDPOINT: str
    USER: str
    APPLICATION: str
    SUBSCRIPTION_KEY: str
    ENV: str
    ALLOWED_HOST: str
    SUMA_ASEGURADA: int
    SM_PRIMARY_PASARELA_KEY: str
    SM_ENDPOINT_PASARELA_MS: str
    SM_PRIMARY_SUSCRIPTION_KEY: str
    SM_ENDPOINT_SUSCRIPCION: str
    MID: str
    MOCKUP: bool
    SM_ENDPOINT_NOTIFICACION_PAGO: str
    SM_NOTIFICACION_PAGO_KEY: str
    MONGO_URI: str
    URL_ANULAR_POLIZA: str
    API_KEY_ANULAR_POLIZA: str

    # Campos opcionales para MCP (con valores por defecto)
    JWT_SECRET_KEY: str | None = None
    BACKEND_BASE_URL: str | None = None
    API_TOKEN_MCP: str | None = None


    # Load the settings from the .env file
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
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
            "API_TOKEN_MCP no está configurado en el archivo .env"
            "Por favor, agregue API_TOKEN_MCP a su archivo .env para usar el MCP."
        )
    return settings.API_TOKEN_MCP


# Assign the settings to variables
API_KEY_AUTH = settings.API_KEY_AUTH
SM_PRIMARY_KEY = settings.SM_PRIMARY_KEY
SM_SECONDARY_KEY = settings.SM_SECONDARY_KEY
SM_ENDPOINT = settings.SM_ENDPOINT
USER = settings.USER
APPLICATION = settings.APPLICATION
SUBSCRIPTION_KEY = settings.SUBSCRIPTION_KEY
ENV = settings.ENV
ALLOWED_HOST = settings.ALLOWED_HOST
SUMA_ASEGURADA = settings.SUMA_ASEGURADA
SM_PRIMARY_PASARELA_KEY = settings.SM_PRIMARY_PASARELA_KEY
SM_ENDPOINT_PASARELA_MS = settings.SM_ENDPOINT_PASARELA_MS
MID = settings.MID
MOCKUP = settings.MOCKUP
SM_PRIMARY_SUSCRIPTION_KEY = settings.SM_PRIMARY_SUSCRIPTION_KEY
SM_ENDPOINT_SUSCRIPCION = settings.SM_ENDPOINT_SUSCRIPCION
SM_ENDPOINT_NOTIFICACION_PAGO = settings.SM_ENDPOINT_NOTIFICACION_PAGO
SM_NOTIFICACION_PAGO_KEY = settings.SM_NOTIFICACION_PAGO_KEY
MONGO_URI = settings.MONGO_URI
URL_ANULAR_POLIZA = settings.URL_ANULAR_POLIZA
API_KEY_ANULAR_POLIZA = settings.API_KEY_ANULAR_POLIZA


def get_valid_api_keys() -> list[str]:
    valid_keys = [API_KEY_AUTH]
    
    # Agregar el token MCP si está configurado (para que el MCP pueda autenticarse)
    if settings.API_TOKEN_MCP:
        valid_keys.append(settings.API_TOKEN_MCP)
    
    return valid_keys
# Log that the settings have been loaded
logger.info("Settings loaded")
