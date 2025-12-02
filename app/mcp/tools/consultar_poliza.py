from typing import Any
from app.mcp.schemas import ConsultarPolizaInput, MCPResponse
from app.mcp.client import get_backend_client
from app.mcp.exceptions import MCPError, ValidationError, MCPErrorAuth
from app.utils.v1.LoggerSingleton import logger
from app.utils.v1.configs import get_mcp_api_token

# Schema JSON para la herramienta
CONSULTAR_POLIZA_SCHEMA = {
    "type": "object",
    "properties": {
        "cd_entidad": {
            "type": "integer",
            "description": "Código de entidad",
            "minimum": 1
        },
        "cd_area": {
            "type": "integer",
            "description": "Código de área",
            "minimum": 1
        },
        "poliza": {
            "type": "integer",
            "description": "Número de póliza",
            "minimum": 1
        },
        "certificado": {
            "type": "integer",
            "description": "Número de certificado",
            "minimum": 1
        },
        "nu_recibo": {
            "type": "integer",
            "description": "Número de recibo (opcional)",
            "minimum": 1
        }
    },
    "required": ["cd_entidad", "cd_area", "poliza", "certificado"]
}


async def consultar_poliza_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    """Maneja la consulta de información de una póliza."""
    try:
        # Validar entrada
        input_data = ConsultarPolizaInput(**arguments)

        # Llamar al backend
        client = get_backend_client()
        backend_data = {
            "cd_entidad": input_data.cd_entidad,
            "cd_area": input_data.cd_area,
            "poliza": input_data.poliza,
            "certificado": input_data.certificado
        }
        
        if input_data.nu_recibo is not None:
            backend_data["nu_recibo"] = input_data.nu_recibo

        try:
            api_token = get_mcp_api_token()
            response = await client.post(
                endpoint="/api/v1/sm/consultar_poliza",
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
            logger.error(f"Error al consultar póliza: {e}")
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
        logger.error(f"Error inesperado en consultar_poliza: {e}")
        return MCPResponse(
            success=False,
            error=f"Error inesperado: {str(e)}",
            code="INTERNAL_ERROR"
        ).model_dump()