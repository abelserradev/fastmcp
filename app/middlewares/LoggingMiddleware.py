from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.v1.LoggerSingleton import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response}")
        logger.info(f"Response status: {response.status_code}")
        return response
