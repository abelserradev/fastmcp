"""Excepciones personalizadas para el módulo MCP."""


class MCPError(Exception):
    """Excepción base para errores del servidor MCP."""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(MCPError):
    """Error de autenticación."""

    def __init__(self, message: str = "Error de autenticación"):
        super().__init__(message, "AUTH_ERROR")


class ValidationError(MCPError):
    """Error de validación de parámetros."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")


class BackendError(MCPError):
    """Error al comunicarse con el backend."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, "BACKEND_ERROR")


class NotFoundError(MCPError):
    """Recurso no encontrado."""

    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, "NOT_FOUND")


class MCPErrorAuth(MCPError):
    def __init__(self, message: str = "Error de configuración del MCP"):
        super().__init__(message, "Falta token de autenticación del MCP") # Se debe tener en el .env el token_MCP
    
