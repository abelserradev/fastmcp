from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.LoggerSingleton import logger
from app.api.Integration_SM.app import router as api_router
app = FastAPI(
    title="Asistensi Integración Seguros Mercantil",  # The title of the API
    description="Asistensi Integración Seguros Mercantil",  # The description of the API
    version="0.1.0",  # The version of the API
    docs_url="/docs",  # The URL where the API documentation will be served
    redoc_url=None,  # The URL where the ReDoc documentation will be served. None means it will not be served
    cors_allowed_origins="*",  # The origins that are allowed to make cross-origin requests
    cors_allowed_methods="*", # Allow all methods
    allow_credentials=True,
    allow_headers="*",
)

# Add a middleware for handling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router, prefix="/api/v1/sm")

logger.info("API started")