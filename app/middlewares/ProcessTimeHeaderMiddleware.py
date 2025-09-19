import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.v2.LoggerSingletonDB import logger

class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.process_time()
        response = await call_next(request)
        process_time = (time.process_time() - start_time) * 10**3
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Response Process Time: {str(process_time)} ms")
        return response
