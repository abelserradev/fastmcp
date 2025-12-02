import pytest
from unittest.mock import Mock, patch, AsyncMock

from app.mcp.tools.consultar_persona import consultar_persona_handler
from app.mcp.tools.consultar_cotizacion import consultar_cotizacion_handler
from app.mcp.tools.consultar_poliza import consultar_poliza_handler


class TestConsultarPersona:
    @pytest.mark.asyncio
    async def test_retorna_exito_con_datos_validos(self, valid_token, mock_backend_client):
        args = {"num_documento": "V-12345678", "token": valid_token}
        mock_response = {"persona": {"nombre": "Test User"}}
        mock_backend_client.post = AsyncMock(return_value=mock_response)

        with patch("app.mcp.tools.consultar_persona.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_persona.get_jwt_handler") as mock_jwt:
            jwt_mock = Mock()
            jwt_mock.decode_token = Mock(return_value={"user_id": "test"})
            mock_jwt.return_value = jwt_mock

            result = await consultar_persona_handler(args)

        assert result["success"] is True
        assert result["data"] == mock_response
        assert result["error"] is None

    @pytest.mark.asyncio
    async def test_retorna_error_con_token_invalido(self, invalid_token):
        args = {"num_documento": "V-12345678", "token": invalid_token}
        result = await consultar_persona_handler(args)

        assert result["success"] is False
        assert result["code"] == "AUTH_ERROR"
        assert result["error"] is not None

    @pytest.mark.asyncio
    async def test_retorna_error_con_documento_invalido(self, valid_token):
        args = {"num_documento": "INVALID", "token": valid_token}
        result = await consultar_persona_handler(args)

        assert result["success"] is False
        assert result["code"] in ["VALIDATION_ERROR", "INTERNAL_ERROR"]


class TestConsultarCotizacion:
    @pytest.mark.asyncio
    async def test_retorna_exito_con_datos_validos(self, valid_token, mock_backend_client):
        args = {"nu_cotizacion": 12345, "cd_entidad": 1, "token": valid_token}
        mock_response = {"cotizacion": {"nu_cotizacion": 12345}}
        mock_backend_client.post = AsyncMock(return_value=mock_response)

        with patch("app.mcp.tools.consultar_cotizacion.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_cotizacion.get_jwt_handler") as mock_jwt:
            jwt_mock = Mock()
            jwt_mock.decode_token = Mock(return_value={"user_id": "test"})
            mock_jwt.return_value = jwt_mock

            result = await consultar_cotizacion_handler(args)

        assert result["success"] is True
        assert result["data"] == mock_response

    @pytest.mark.asyncio
    async def test_retorna_error_con_cotizacion_invalida(self, valid_token):
        args = {"nu_cotizacion": 0, "cd_entidad": 1, "token": valid_token}
        result = await consultar_cotizacion_handler(args)

        assert result["success"] is False
        assert result["code"] in ["VALIDATION_ERROR", "INTERNAL_ERROR"]


class TestConsultarPoliza:
    @pytest.mark.asyncio
    async def test_retorna_exito_con_datos_validos(self, valid_token, mock_backend_client):
        args = {
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
            jwt_mock = Mock()
            jwt_mock.decode_token = Mock(return_value={"user_id": "test"})
            mock_jwt.return_value = jwt_mock

            result = await consultar_poliza_handler(args)

        assert result["success"] is True
        assert result["data"] == mock_response

    @pytest.mark.asyncio
    async def test_incluye_recibo_cuando_se_proporciona(self, valid_token, mock_backend_client):
        args = {
            "cd_entidad": 1,
            "cd_area": 1,
            "poliza": 12345,
            "certificado": 1,
            "nu_recibo": 10,
            "token": valid_token
        }
        mock_response = {"poliza": {"nu_poliza": 12345}}
        mock_backend_client.post = AsyncMock(return_value=mock_response)

        with patch("app.mcp.tools.consultar_poliza.get_backend_client", return_value=mock_backend_client), \
             patch("app.mcp.tools.consultar_poliza.get_jwt_handler") as mock_jwt:
            jwt_mock = Mock()
            jwt_mock.decode_token = Mock(return_value={"user_id": "test"})
            mock_jwt.return_value = jwt_mock

            result = await consultar_poliza_handler(args)

        assert result["success"] is True
        call_args = mock_backend_client.post.call_args
        assert "nu_recibo" in call_args[1]["data"]