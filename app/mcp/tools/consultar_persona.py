from typing import Any
from app.mcp.schemas import ConsultarPersonaInput
from app.mcp.client import get_backend_client
from app.utils.v1.configs import get_mcp_api_token


# Schema JSON para la herramienta
CONSULTAR_PERSONA_SCHEMA = {
    "type": "object",
    "properties": {
        "num_documento": {
            "type": "string",
            "description": "Número de documento de la persona (formato: V-12345678, E-12345678, P-12345678)",
            "pattern": "^[VEP]-\\d{5,30}$"
        }
    },
    "required": ["num_documento"]
}


async def consultar_persona_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    """Maneja la consulta de información de una persona."""
    # Validar entrada
    input_data = ConsultarPersonaInput(**arguments)

    # Llamar al backend
    client = get_backend_client()
    backend_data = {
        "num_documento": input_data.num_documento
    }

    api_token = get_mcp_api_token()
    response = await client.post(
        endpoint="/api/v1/sm/consultar_persona",
        data=backend_data,
        api_key=api_token  
    )

    # Devolver directamente los datos (FastMCP maneja los errores con excepciones)
    return response