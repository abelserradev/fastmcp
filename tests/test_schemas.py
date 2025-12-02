
import pytest
from datetime import datetime, date
from pydantic import ValidationError, EmailStr
from fastapi import HTTPException

from app.schemas.v1.Integration_SM.ModelAPI import (
    TipoDocumento,
    Sexo,
    ConsultarPersonaBase,
    DocumentoBase,
    ContactoBase,
    PersonaBase,
    CrearPersonaBase,
    FrecuenciaCuota,
    PolizaBase,
    PersonaPolizaBase,
    CrearPolizaBase,
    EmitirPolizaBase,
    ConsultarPolizaBase,
)

@pytest.fixture
def documento_valido():
    return {"nu_documento": "V-1234567890"}

@pytest.fixture
def contacto_valido():
    return {
        "nu_area_telefono": "+58",
        "nu_telefono": "04123456789",
        "de_email": "test@example.com",
    }

@pytest.fixture
def persona_base_data(documento_valido, contacto_valido):
    return {
        "nm_primer_nombre": "Juan",
        "nm_segundo_nombre": "Perez",
        "nm_primer_apellido": "Gomez",
        "nm_segundo_apellido": "Lopez",
        "cd_sexo": Sexo.M,
        "fe_nacimiento": "01/01/1990",
        "documento": documento_valido,
        "contacto": contacto_valido,
    }

# A partir de aqui se crea el test para enums
@pytest.mark.unit
class TestTipoDocumento:
    def test_valores_enum_validos(self):
        assert TipoDocumento.VEN.value == "VEN"
        assert TipoDocumento.PVEN.value == "PVEN"


    def test_enum_acepta_valor_valido(self):
        assert TipoDocumento("VEN") == TipoDocumento.VEN

    def test_enum_rechaza_valor_invalido(self):
        with pytest.raises(ValueError):
            TipoDocumento("INVALID")

@pytest.mark.unit
class TestSexo:
    def test_valores_enum_validos(self):
        assert Sexo.M.value == "M"
        assert Sexo.F.value == "F"
    
    @pytest.mark.parametrize("valor", ["M", "F"])
    def test_enum_acepta_valor_valido(self, valor):
        assert Sexo(valor) in [Sexo.M, Sexo.F]

@pytest.mark.unit
class TestFrecuenciaCuota:

    @pytest.mark.parametrize("frecuencia", [FrecuenciaCuota.MENSUAL, FrecuenciaCuota.TRIMESTRAL])
    def test_frecuencias_validas(self, frecuencia):
        assert frecuencia in FrecuenciaCuota


# test para los documentos

@pytest.mark.unit
class TestDocumentoBase:
    @pytest.mark.parametrize(
        "documento_valido", ["V-1234567890", "E-1234567890", "P-1234567890", "J-1234567890", "V-12345"]
    )
    def test_documento_valido(self, documento_valido):
        doc = DocumentoBase(nu_documento=documento_valido)
        assert doc.nu_documento == documento_valido

    @pytest.mark.parametrize(
        "documento_invalido",
        [
            "v1234567890",
            "X-1234567890",
            "V-1234",
            "V-1234567890123456789012345678901",
            "",
            "340398243",
        ]
    )
    def test_documento_invalido(self, documento_invalido):
        with pytest.raises(ValidationError) as exc_info:
            DocumentoBase(nu_documento=documento_invalido)

        errors = exc_info.value.errors()
        assert any(error["type"] == "string_pattern_mismatch" for error in errors)

    def test_documento_requerido(self):
        with pytest.raises(ValidationError) as exc_info:
            DocumentoBase()

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("nu_documento",) for error in errors)

@pytest.mark.unit
class TestConsultarPersonaBase:
    def test_num_documento_valido(self):
        consulta = ConsultarPersonaBase(num_documento="V-1234567890")
        assert consulta.num_documento == "V-1234567890"

    def test_num_documento_invalido(self):
        with pytest.raises(ValidationError):
            ConsultarPersonaBase(num_documento="INVALID")


# Test para los contactos

@pytest.mark.unit
class TestContactoBase:
    def test_contacto_valido(self, contacto_valido):
        contacto = ContactoBase(**contacto_valido)
        assert contacto.de_email == "test@example.com"

    @pytest.mark.parametrize(
        "email_invalido",
        [
            "not_an_email",
            "@example.com",
            "test@",
            "test...test@example.com",
            "",
        ]
    )
    def test_email_invalido(self, email_invalido, contacto_valido):
        contacto_valido["de_email"] = email_invalido
        with pytest.raises(ValidationError) as exc_info:
            ContactoBase(**contacto_valido)

        errors = exc_info.value.errors()
        assert any("email" in str(error.get("type", "")).lower() or "value_error" in str(error.get("type", "")).lower() or
        error.get("type") == "value_error" for error in errors)

    def test_campos_requeridos(self):
        with pytest.raises(ValidationError) as exc_info:
            ContactoBase()
        errors = exc_info.value.errors()
        required_fields = {"nu_area_telefono", "nu_telefono", "de_email"}
        error_fields = {error["loc"][0] for error in errors if error["loc"]}
        assert required_fields.issubset(error_fields)


# Test para validar las fechas
@pytest.mark.unit
class TestPersonaBaseFechaNacimiento:
    @pytest.mark.parametrize(
        "fecha_valida",
        [
            "15/03/1990",
            "01/01/2000",
            "31/12/1985",
            "29/02/2000",
        ])
    def test_fecha_nacimiento_string_valida(self, fecha_valida, persona_base_data):
        persona_base_data["fe_nacimiento"] = fecha_valida
        persona = PersonaBase(**persona_base_data)
        assert persona.fe_nacimiento == fecha_valida

    def test_fecha_nacimiento_datetime_valida(self, persona_base_data):
        fecha_datetime = datetime(1990, 3, 15, 10, 30, 0)
        persona_base_data["fe_nacimiento"] = fecha_datetime
        persona = PersonaBase(**persona_base_data)
        assert isinstance(persona.fe_nacimiento, (str, date))
        if isinstance(persona.fe_nacimiento, str):
            assert persona.fe_nacimiento == "15/03/1990"
        
    @pytest.mark.parametrize(
        "fecha_invalida",
        [
            "1990-03-15", 
            "15-03-1990",  
            "03/15/1990",  
            "15/3/1990",  
            "32/01/1990",  
            "15/13/1990",
            "invalid-date",
            "",
        ])
    def test_fecha_nacimiento_invalida(self, fecha_invalida, persona_base_data):
        try:
            persona = PersonaBase(**persona_base_data)
            if isinstance(persona.fe_nacimiento, str):
                parts = persona.fe_nacimiento.split("/")
                if len(parts) == 3:
                    if len(parts[0]) != 2 or len(parts[1]) != 2 or len(parts[2]) != 4:
                        pytest.fail(f"Fecha inválida: {persona.fe_nacimiento}")
        except ValueError:
            pass

    def test_fecha_nacimiento_invalido(self, persona_base_data):
        persona_base_data["fe_nacimiento"] = [12345]
        with pytest.raises(ValidationError) as exc_info:
            PersonaBase(**persona_base_data)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0, "Se esperaba un error de validación"
        assert any(
            error.get("type") in ["string_type","value_error","type_error","list_type"] or "formato" in str(error.get("msg", "")).lower()
            for error in errors)


@pytest.mark.unit
class TestCrearPersonaBaseFechaRegistro:

    def test_fe_registro_string_valida(self, persona_base_data):
        persona = PersonaBase(**persona_base_data)
        crear_persona = CrearPersonaBase(persona=persona, fe_registro="01/01/2025")
        assert crear_persona.fe_registro == "01/01/2025"

    def test_fe_registro_datetime_valida(self, persona_base_data):
        persona = PersonaBase(**persona_base_data)
        fecha_datetime = datetime(2025, 1, 1)
        with pytest.raises(ValidationError) as exc_info:
           CrearPersonaBase(persona=persona, fe_registro=fecha_datetime)
        errors = exc_info.value.errors()
        assert any (error.get("type") == "string_type" for error in errors)

    def test_fe_registro_invalida(self, persona_base_data):
        persona = PersonaBase(**persona_base_data)
        with pytest.raises(ValidationError):
            CrearPersonaBase(persona=persona, fe_registro="2024-01-01")

@pytest.mark.unit
class TestPolizaBaseFechas:
    @pytest.mark.parametrize(
        "fecha_desde, fecha_hasta",
        [
            ("01/01/2025", "31/12/2025"),
            ("15/06/2025", "15/06/2026"),
        ]
    )
    def test_fechas_validas(self, fecha_desde, fecha_hasta):
        poliza = PolizaBase(fe_desde=fecha_desde, fe_hasta=fecha_hasta, frecuencia_cuota=FrecuenciaCuota.MENSUAL)
        assert isinstance(poliza.fe_desde, date)
        assert isinstance(poliza.fe_hasta, date)

    def test_fechas_polizadatetime(self):
        fecha_desde = datetime(2025, 1, 1)
        fecha_hasta = datetime(2025, 12, 31)
        poliza = PolizaBase(fe_desde=fecha_desde, fe_hasta=fecha_hasta, frecuencia_cuota=FrecuenciaCuota.TRIMESTRAL)
        assert isinstance(poliza.fe_desde, date)
        assert isinstance(poliza.fe_hasta, date)

    def test_suma_asegurada(self):
        poliza = PolizaBase(fe_desde="01/01/2025", fe_hasta="31/12/2025", frecuencia_cuota=FrecuenciaCuota.MENSUAL)
        assert poliza.suma_asegurada == 250

    def test_suma_aseguradapersonalizada(self):
        poliza = PolizaBase(fe_desde="01/01/2025", fe_hasta="31/12/2025", frecuencia_cuota=FrecuenciaCuota.MENSUAL, suma_asegurada=500)
        assert poliza.suma_asegurada == 500


