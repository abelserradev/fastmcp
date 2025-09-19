from fastapi import FastAPI,Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.Integration_SM.app import router as api_router_v1
from app.middlewares.ConfigureMiddleware import configure_middleware
from app.api.v2.Integration_SM.app import router as api_router_v2
from app.api.v3.Integration_SM.app import router as api_router_v3
from app.api.v4.Integration_SM.app import router as api_router_v4
from app.api.v5.Integration_SM.app import router as api_router_v5
from app.api.v1.PasarelaPagoMS.app import router as api_router_pasarela_ms_v1
from app.api.v2.PasarelaPagoMS.app import router as api_router_pasarela_ms_v2
from app.utils.v2.LoggerSingletonDB import logger

app = FastAPI(
    title="Asistensi Integración Seguros Mercantil",  # The title of the API
    description="Asistensi Integración Seguros Mercantil",  # The description of the API
    version="0.1.0",  # The version of the API
    docs_url="/docs",  # The URL where the API documentation will be served
    redoc_url=None  # The URL where the ReDoc documentation will be served. None means it will not be served
)


configure_middleware(app)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Este manejador se activa cada vez que una validación de Pydantic falla.
    `exc` es la instancia de la excepción original `RequestValidationError`.
    """
    # Obtenemos los detalles del error en un formato legible
    error_details = exc.errors()

    # Loggeamos los detalles del error en el servidor. ¡Esto es lo que necesitas!
    logger.error(f"Error de validación en la petición: {request.method} {request.url}")
    logger.error(f"Payload recibido (cuerpo): {await request.body()}")
    logger.error(f"Detalles del error de Pydantic: {error_details}")

    # Podemos incluso modificar la respuesta que se envía al cliente si quisiéramos.
    # Por ahora, simplemente replicaremos el comportamiento por defecto de FastAPI,
    # que es devolver los detalles del error.
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_details},
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: A dictionary with a status message.
    """
    return {"status": "ok"}


app.include_router(api_router_v1, prefix="/api/v1/sm")
app.include_router(api_router_v2, prefix="/api/v2/sm")
app.include_router(api_router_v3, prefix="/api/v3/sm")
app.include_router(api_router_v4, prefix="/api/v4/sm")
app.include_router(api_router_v5, prefix="/api/v5/sm")
app.include_router(api_router_pasarela_ms_v1,prefix="/api/v1/pasarela_pago_ms")
app.include_router(api_router_pasarela_ms_v2,prefix="/api/v2/pasarela_pago_ms")

logger.info("API started")
