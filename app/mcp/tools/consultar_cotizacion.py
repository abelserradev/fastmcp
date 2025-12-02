from typing import Any
from app.mcp.schemas import ConsultarCotizacionInput
from app.mcp.client import get_backend_client
from app.utils.v1.configs import get_mcp_api_token


# Schema JSON para la herramienta
CONSULTAR_COTIZACION_SCHEMA = {
    "type": "object",
    "properties": {
        "nu_cotizacion": {
            "type": "integer",
            "description": "Número de cotización",
            "minimum": 1
        },
        "cd_entidad": {
            "type": "integer",
            "description": "Código de entidad",
            "minimum": 1
        }
    },
    "required": ["nu_cotizacion", "cd_entidad"]
}


async def consultar_cotizacion_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    """Maneja la consulta de información de una cotización."""
    # Validar entrada
    input_data = ConsultarCotizacionInput(**arguments)

    # Llamar al backend
    client = get_backend_client()
    backend_data = {
        "nu_cotizacion": input_data.nu_cotizacion,
        "cd_entidad": input_data.cd_entidad
    }

    api_token = get_mcp_api_token()
    response = await client.post(
        endpoint="/api/v2/sm/consultar_cotizacion",
        data=backend_data,
        api_key=api_token
    )

    # Devolver directamente los datos (FastMCP maneja los errores con excepciones)
    return response