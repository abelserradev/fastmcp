"""Herramientas MCP."""

from app.mcp.tools.consultar_persona import consultar_persona_handler
from app.mcp.tools.consultar_cotizacion import consultar_cotizacion_handler
from app.mcp.tools.consultar_poliza import consultar_poliza_handler

__all__ = [
    "consultar_persona_handler",
    "consultar_cotizacion_handler",
    "consultar_poliza_handler",
]