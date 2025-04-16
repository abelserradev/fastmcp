from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.v1.LoggerSingleton import logger


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


    # Load the settings from the .env file
    model_config = SettingsConfigDict(env_file=".env")


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
# Log that the settings have been loaded
logger.info("Settings loaded")
