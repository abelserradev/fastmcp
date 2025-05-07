import uvicorn

from app.utils.v1.LoggerSingleton import logger
from app.utils.v1.configs import ENV
from app.utils.v1.constants import (
    url_consult_persona,
    url_crear_persona,
    url_crear_cotizacion,
    url_emitir_poliza,
    url_consultar_poliza,
    url_inclusion_anexos_poliza,
    url_cotizar,
    url_consultar_cotizacion,
    url_registrar_pago,
    url_otp_mbu,
    url_notificacion_pago,
    url_suscripcion_tasa_bcv,
    url_cuadro_poliza,
)


def main():
    """
    Main function to initialize and start the server.

    This function logs server environment details and settings URLs for different services.
    It then starts the server in the configured environment mode. For production and staging
    environments, the server runs with no reload and multiple workers. For other environments,
    the server runs with the reload option enabled.

    Attributes:
        ENV (str): The current environment of the server (e.g., production, staging,
            development).
        url_consult_persona (str): The URL to consult person data.
        url_crear_persona (str): The URL to create person data.
        url_crear_cotizacion (str): The URL to create a quotation.
        url_emitir_poliza (str): The URL to issue a policy.
        url_inclusion_anexos_poliza (str): The URL for the inclusion of policy annexes.
        url_cotizar (str): The URL to perform a quotation.
        url_consultar_cotizacion (str): The URL to consult quotations.
        url_registrar_pago (str): The URL to register payments.
        url_otp_mbu (str): The URL to generate OTPs.
        url_notificacion_pago (str): The URL to notify payments.
        url_suscripcion_tasa_bcv (str): The URL to consult BCV rates.
        url_cuadro_poliza (str): The URL to generate a policy overview.

    Raises:
        Exception: If any error occurs during server initialization or while starting
            the server.

    """
    logger.info("Server started")
    logger.info(f"Environment: {ENV}")
    logger.info("Loading settings")
    logger.info(f"URL consultar persona: {url_consult_persona}")
    logger.info(f"URL crear persona: {url_crear_persona}")
    logger.info(f"URL crear cotización: {url_crear_cotizacion}")
    logger.info(f"URL emitir poliza: {url_emitir_poliza}")
    logger.info(f"URL inclusión anexos póliza: {url_inclusion_anexos_poliza}")
    logger.info(f"URL cotizar: {url_cotizar}")
    logger.info(f"URL consultar cotización: {url_consultar_cotizacion}")
    logger.info(f"URL registrar pago: {url_registrar_pago}")
    logger.info(f"URL generar otp: {url_otp_mbu}")
    logger.info(f"URL notificar pago: {url_notificacion_pago}")
    logger.info(f"URL consultar Tasa BCV: {url_suscripcion_tasa_bcv}")
    logger.info(f"URL cuadro de póliza: {url_cuadro_poliza}")

    if ENV in ["production", "staging"]:

        uvicorn.run("app.api.app:app", host="0.0.0.0", port=9000, reload=False, workers=4)
    else:
        uvicorn.run("app.api.app:app", host="0.0.0.0", port=9000, reload=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped")
