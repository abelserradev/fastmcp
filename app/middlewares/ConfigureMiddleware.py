from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app import middlewares
from app.utils.v1.constants import CORS_CONFIG

# from starlette_csrf import CSRFMiddleware



def configure_middleware(app):
    """Configure middleware for the FastAPI app."""
    app.add_middleware(CORSMiddleware, **CORS_CONFIG)
    app.add_middleware(
        GZipMiddleware, minimum_size=1000
    )  # Compress responses larger than 1000 bytes


    # app.add_middleware(CSRFMiddleware, secret="__CHANGE_ME__")
    # Los middlewares personalizados
    #app.add_middleware(middlewares.ErrorHandlingMiddleware)
    #app.add_middleware(middlewares.LoggingMiddleware)
    app.add_middleware(middlewares.ProcessTimeHeaderMiddleware)
    # if ENV in ["production", "staging"]:
        # app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOST)
        #app.add_middleware(HTTPSRedirectMiddleware)
