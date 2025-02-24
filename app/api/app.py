from fastapi import FastAPI

from app.api.v1.Integration_SM.app import router as api_router_v1
from app.middlewares.ConfigureMiddleware import configure_middleware
from app.api.v2.Integration_SM.app import router as api_router_v2
from app.api.v3.Integration_SM.app import router as api_router_v3
from app.api.v1.PasarelaPagoMS.app import router as api_router_pasarela_ms_v1
from app.utils.v1.LoggerSingleton import logger

app = FastAPI(
    title="Asistensi Integración Seguros Mercantil",  # The title of the API
    description="Asistensi Integración Seguros Mercantil",  # The description of the API
    version="0.1.0",  # The version of the API
    docs_url="/docs",  # The URL where the API documentation will be served
    redoc_url=None  # The URL where the ReDoc documentation will be served. None means it will not be served
)


configure_middleware(app)



app.include_router(api_router_v1, prefix="/api/v1/sm")
app.include_router(api_router_v2, prefix="/api/v2/sm")
app.include_router(api_router_v3, prefix="/api/v3/sm")
app.include_router(api_router_pasarela_ms_v1,prefix="/api/v1/pasarela_pago_ms")

logger.info("API started")
