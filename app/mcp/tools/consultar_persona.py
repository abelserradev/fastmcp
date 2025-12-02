from typing import Any
from app.mcp.schemas import ConsultarPersonaInput, MCPResponse
from app.mcp.client import get_backend_client
from app.mcp.exceptions import MCPError, ValidationError, MCPErrorAuth
from app.utils.v1.LoggerSingleton import logger
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
    try:
        # Validar entrada
        input_data = ConsultarPersonaInput(**arguments)

        # Llamar al backend
        client = get_backend_client()
        backend_data = {
            "num_documento": input_data.num_documento
        }

        try:
            api_token = get_mcp_api_token()
            response = await client.post(
                endpoint="/api/v1/sm/consultar_persona",
                data=backend_data,
                api_key=api_token  
            )

            return MCPResponse(
                success=True,
                data=response
            ).model_dump()

        except MCPErrorAuth as e:
            logger.error(f"Error de configuración: {e}")
            return MCPResponse(
                success=False,
                error=str(e),
                code=e.code or "CONFIGURATION_ERROR"
            ).model_dump()
        except Exception as e:
            logger.error(f"Error al consultar persona: {e}")
            error_code = "BACKEND_ERROR"
            if isinstance(e, MCPError):
                error_code = e.code or "BACKEND_ERROR"
            
            return MCPResponse(
                success=False,
                error=str(e),
                code=error_code
            ).model_dump()

    except ValidationError as e:
        return MCPResponse(
            success=False,
            error=f"Error de validación: {str(e)}",
            code="VALIDATION_ERROR"
        ).model_dump()
    except Exception as e:
        logger.error(f"Error inesperado en consultar_persona: {e}")
        return MCPResponse(
            success=False,
            error=f"Error inesperado: {str(e)}",
            code="INTERNAL_ERROR"
        ).model_dump()