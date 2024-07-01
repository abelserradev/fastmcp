from fastapi import FastAPI


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


@app.get("/")
def read_root():
    return {"Hello": "World"}