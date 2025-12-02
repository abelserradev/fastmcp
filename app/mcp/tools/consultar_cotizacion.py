from typing import Any
from app.mcp.schemas import ConsultarCotizacionInput, MCPResponse
from app.mcp.client import get_backend_client
from app.mcp.exceptions import MCPError, ValidationError, MCPErrorAuth
from app.utils.v1.LoggerSingleton import logger
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
    try:
        # Validar entrada
        input_data = ConsultarCotizacionInput(**arguments)

        # Llamar al backend
        client = get_backend_client()
        backend_data = {
            "nu_cotizacion": input_data.nu_cotizacion,
            "cd_entidad": input_data.cd_entidad
        }

        try:
            api_token = get_mcp_api_token()
            response = await client.post(
                endpoint="/api/v2/sm/consultar_cotizacion",
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
            logger.error(f"Error al consultar cotización: {e}")
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
        logger.error(f"Error inesperado en consultar_cotizacion: {e}")
        return MCPResponse(
            success=False,
            error=f"Error inesperado: {str(e)}",
            code="INTERNAL_ERROR"
        ).model_dump()