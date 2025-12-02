"""Servidor MCP principal."""

import os
import sys

# IMPORTANTE: Establecer esta variable ANTES de cualquier importación que use el logger
# Los servidores MCP usan stdout para JSON, así que los logs deben ir a stderr y sin colores
os.environ["MCP_SERVER_MODE"] = "true"

from fastmcp import FastMCP
from typing import Optional
from app.mcp.tools import (
    consultar_persona_handler,
    consultar_cotizacion_handler,
    consultar_poliza_handler,
)

mcp = FastMCP("Seguros Mercantil MCP Server")


@mcp.tool()
async def consultar_persona(
    num_documento: str,
) -> dict:
    """
    Consulta información de una persona en Seguros Mercantil utilizando su número de documento.
    
    Args:
        num_documento: Número de documento de la persona (formato: V-12345678, E-12345678, P-12345678)
    
    Returns:
        dict: Respuesta estructurada con la información de la persona
    """
    return await consultar_persona_handler({
        "num_documento": num_documento,
    })


@mcp.tool()
async def consultar_cotizacion(
    nu_cotizacion: int,
    cd_entidad: int,
) -> dict:
    """
    Consulta información de una cotización en Seguros Mercantil.
    
    Args:
        nu_cotizacion: Número de cotización
        cd_entidad: Código de entidad
    
    Returns:
        dict: Respuesta estructurada con la información de la cotización
    """
    return await consultar_cotizacion_handler({
        "nu_cotizacion": nu_cotizacion,
        "cd_entidad": cd_entidad,
    })


@mcp.tool()
async def consultar_poliza(
    cd_entidad: int,
    cd_area: int,
    poliza: int,
    certificado: int,
    nu_recibo: Optional[int] = None
) -> dict:
    """
    Consulta información de una póliza en Seguros Mercantil.
    
    Args:
        cd_entidad: Código de entidad
        cd_area: Código de área
        poliza: Número de póliza
        certificado: Número de certificado
        nu_recibo: Número de recibo (opcional)
    
    Returns:
        dict: Respuesta estructurada con la información de la póliza
    """
    args = {
        "cd_entidad": cd_entidad,
        "cd_area": cd_area,
        "poliza": poliza,
        "certificado": certificado,
    }
    if nu_recibo is not None:
        args["nu_recibo"] = nu_recibo
    return await consultar_poliza_handler(args)


if __name__ == "__main__":
    mcp.run()
