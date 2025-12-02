

import httpx
from typing import Any, Optional, Dict

from app.mcp.exceptions import BackendError, NotFoundError
from app.utils.v1.configs import get_settings
from app.utils.v1.LoggerSingleton import logger


class BackendClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 180.0,
        headers: Optional[Dict[str, str]] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = headers or {}

    async def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        token: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.default_headers}

        if api_key:
            request_headers["X-API-Key"] = api_key
            logger.info(f"X-API-Key configurada: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else ''}")
        elif token:
            request_headers["Authorization"] = f"Bearer {token}"

        if headers:
            request_headers.update(headers)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Request POST {url}")
                logger.info(f"Headers enviados: {list(request_headers.keys())}")
                logger.info(f"Data: {data}")
                response = await client.post(
                    url,
                    json=data,
                    headers=request_headers,
                )
                logger.info(f"Response {response.status_code}: {response.text[:500]}")

                if response.status_code == 404:
                    raise NotFoundError("Recurso no encontrado")
                
                if response.status_code >= 400:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = error_json.get("detail", error_json.get("message", error_detail))
                    except Exception:
                        pass
                    raise BackendError(
                        f"Error del backend: {error_detail}",
                        status_code=response.status_code
                    )
                return response.json()
        
        except httpx.TimeoutException as e:
            logger.error(f"Timeout al conectar con el backend: {e}")
            raise BackendError("Timeout al conectar con el backend", status_code=408)
        except httpx.RequestError as e:
            logger.error(f"Error de conexion con backend: {e}")
            raise BackendError("Error de conexion con el backend", status_code=500)

        except NotFoundError as e:
            raise
        except BackendError as e:
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            raise BackendError("Error inesperado al realizar la peticion", status_code=500)

def get_backend_client() -> BackendClient:
    """Obtiene una instancia del cliente backend."""
    settings = get_settings()
    base_url = getattr(settings, "BACKEND_BASE_URL", None) or "http://localhost:9000"
    return BackendClient(base_url=base_url)