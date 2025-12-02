"""Autenticación para el servidor MCP."""

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.v1.configs import get_mcp_local_token
from app.mcp.exceptions import AuthenticationError

# Esquema de seguridad HTTP Bearer para autenticación con token
security = HTTPBearer()


def verify_mcp_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verifica el token de autenticación del cliente MCP.
    
    Similar a la implementación del repositorio Openweather-MCP-server-fastAPI-MCP,
    verifica que el token proporcionado en el header Authorization coincida con
    el MCP_LOCAL_TOKEN configurado en el .env.
    
    Args:
        credentials: Credenciales HTTP Bearer del header Authorization
        
    Returns:
        str: El token verificado
        
    Raises:
        HTTPException: Si el token es inválido o no está configurado
        AuthenticationError: Si hay error en la autenticación
    """
    try:
        expected_token = get_mcp_local_token()
        token = credentials.credentials
        
        if token != expected_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticación inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise AuthenticationError(f"Error al verificar token: {str(e)}")


async def verify_mcp_token_async(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Versión async del verificador de token para el cliente MCP.
    
    Args:
        credentials: Credenciales HTTP Bearer del header Authorization
        
    Returns:
        str: El token verificado
        
    Raises:
        HTTPException: Si el token es inválido o no está configurado
        AuthenticationError: Si hay error en la autenticación
    """
    return verify_mcp_token(credentials)
