import pytest
from unittest.mock import Mock, AsyncMock, patch

from fastmcp import FastMCP
from app.mcp.server import mcp
from app.mcp.tools import (
    consultar_persona_handler,
    consultar_cotizacion_handler,
    consultar_poliza_handler,
)


class TestMCPServer:
    def test_crea_instancia_servidor(self):
        assert mcp is not None
        assert isinstance(mcp, FastMCP)
        assert mcp.name == "Seguros Mercantil MCP Server"

    def test_handlers_disponibles(self):
        assert consultar_persona_handler is not None
        assert consultar_cotizacion_handler is not None
        assert consultar_poliza_handler is not None
        assert callable(consultar_persona_handler)
        assert callable(consultar_cotizacion_handler)
        assert callable(consultar_poliza_handler)

    def test_servidor_tiene_nombre_correcto(self):
        assert mcp.name == "Seguros Mercantil MCP Server"


class TestMCPServerIntegration:
    def _setup_jwt_mock(self, mock_jwt):
        jwt_instance = Mock()
        jwt_instance.decode_token = Mock(return_value={"user_id": "test_user"})
        mock_jwt.return_value = jwt_instance
        return jwt_instance

    @pytest.mark.asyncio
    async def test_ejecuta_consultar_persona(self, valid_token, mock_backend_client):
        arguments = {"num_documento": "V-12345678", "token": valid_token}
        mock_response = {"persona": {"nombre": "Test User"}}
        mock_backend_client.post = AsyncMock(return_value=mock_response)

        with patch("app.mcp.tools.consultar_persona.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_persona.get_jwt_handler") as mock_jwt:
            self._setup_jwt_mock(mock_jwt)
            result = await consultar_persona_handler(arguments)

        assert result["success"] is True
        assert result["data"] == mock_response

    @pytest.mark.asyncio
    async def test_ejecuta_consultar_cotizacion(self, valid_token, mock_backend_client):
        arguments = {"nu_cotizacion": 12345, "cd_entidad": 1, "token": valid_token}
        mock_response = {"cotizacion": {"nu_cotizacion": 12345}}
        mock_backend_client.post = AsyncMock(return_value=mock_response)

        with patch("app.mcp.tools.consultar_cotizacion.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_cotizacion.get_jwt_handler") as mock_jwt:
            self._setup_jwt_mock(mock_jwt)
            result = await consultar_cotizacion_handler(arguments)

        assert result["success"] is True
        assert result["data"] == mock_response

    @pytest.mark.asyncio
    async def test_ejecuta_consultar_poliza(self, valid_token, mock_backend_client):
        arguments = {
            "cd_entidad": 1,
            "cd_area": 1,
            "poliza": 12345,
            "certificado": 1,
            "token": valid_token
        }
        mock_response = {"poliza": {"nu_poliza": 12345}}
        mock_backend_client.post = AsyncMock(return_value=mock_response)

        with patch("app.mcp.tools.consultar_poliza.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_poliza.get_jwt_handler") as mock_jwt:
            self._setup_jwt_mock(mock_jwt)
            result = await consultar_poliza_handler(arguments)

        assert result["success"] is True
        assert result["data"] == mock_response


class TestMCPServerErrorHandling:
    @pytest.mark.asyncio
    async def test_maneja_campos_faltantes(self):
        arguments = {"num_documento": "V-12345678"}
        result = await consultar_persona_handler(arguments)

        assert result["success"] is False
        assert result["code"] in ["VALIDATION_ERROR", "AUTH_ERROR", "INTERNAL_ERROR"]
        assert result["error"] is not None

    @pytest.mark.asyncio
    async def test_maneja_token_invalido(self, invalid_token):
        arguments = {"num_documento": "V-12345678", "token": invalid_token}
        result = await consultar_persona_handler(arguments)

        assert result["success"] is False
        assert result["code"] == "AUTH_ERROR"

    @pytest.mark.asyncio
    async def test_maneja_error_backend(self, valid_token, mock_backend_client):
        from app.mcp.exceptions import BackendError

        arguments = {"num_documento": "V-12345678", "token": valid_token}
        mock_backend_client.post = AsyncMock(side_effect=BackendError("Error del backend", status_code=500))

        with patch("app.mcp.tools.consultar_persona.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_persona.get_jwt_handler") as mock_jwt:
            jwt_instance = Mock()
            jwt_instance.decode_token = Mock(return_value={"user_id": "test_user"})
            mock_jwt.return_value = jwt_instance

            result = await consultar_persona_handler(arguments)

        assert result["success"] is False
        assert result["code"] == "BACKEND_ERROR"
        assert "error" in result


class TestMCPServerResponseFormat:
    async def _ejecutar_handler_exitoso(self, valid_token, mock_backend_client, mock_response):
        arguments = {"num_documento": "V-12345678", "token": valid_token}
        mock_backend_client.post = AsyncMock(return_value=mock_response)

        with patch("app.mcp.tools.consultar_persona.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_persona.get_jwt_handler") as mock_jwt:
            jwt_instance = Mock()
            jwt_instance.decode_token = Mock(return_value={"user_id": "test_user"})
            mock_jwt.return_value = jwt_instance
            return await consultar_persona_handler(arguments)

    @pytest.mark.asyncio
    async def test_respuesta_tiene_formato_estandar(self, valid_token, mock_backend_client):
        mock_response = {"persona": {"nombre": "Test User"}}
        result = await self._ejecutar_handler_exitoso(valid_token, mock_backend_client, mock_response)

        assert "success" in result
        assert isinstance(result["success"], bool)
        assert "data" in result
        assert "error" in result
        assert "code" in result

    @pytest.mark.asyncio
    async def test_respuesta_exitosa_tiene_datos(self, valid_token, mock_backend_client):
        mock_response = {"persona": {"nombre": "Test User"}}
        result = await self._ejecutar_handler_exitoso(valid_token, mock_backend_client, mock_response)

        assert result["success"] is True
        assert result["data"] is not None
        assert result["error"] is None
        assert result["code"] is None

    @pytest.mark.asyncio
    async def test_respuesta_error_tiene_codigo(self, invalid_token):
        arguments = {"num_documento": "V-12345678", "token": invalid_token}
        result = await consultar_persona_handler(arguments)

        assert result["success"] is False
        assert result["data"] is None
        assert result["error"] is not None
        assert result["code"] is not None