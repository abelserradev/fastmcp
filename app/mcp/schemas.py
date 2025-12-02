
from pydantic import BaseModel, Field, field_validator
from typing import Optional


#Schema de entrada para la consulta de una persona
class ConsultarPersonaInput(BaseModel):
    num_documento: str = Field(
        ...,
        description= "Numero de documento de la persona (Formato: V-, E- o J- seguido de 5 a 30 digitos)",
        examples= ["V-12345678"]
    )

    @field_validator("num_documento")
    @classmethod
    def validate_num_documento(cls, v:str ) -> str:
        #Validar el formato del numero de documento
        if not v or len(v) < 5 :
            raise ValueError("El numero de documento debe tener al menos 5 digitos")
        if v[0] not in ["V", "E","P","J"]:
            raise ValueError("El numero de documento debe comenzar con V, E, P o J")
        if v[1] != "-":
            raise ValueError("El numero de documento debe tener un guion")
        return v

# Schema de entrada para la consulta de una cotizacion
class ConsultarCotizacionInput(BaseModel):
    nu_cotizacion: int = Field(
        ...,
        description="Numero de cotizacion de la poliza",
        examples= [12345]
    )
    cd_entidad: int = Field(
        ...,
        description="Codigo de entidad de la cotizacion"
    )

    @field_validator("nu_cotizacion")
    @classmethod
    def validate_nu_cotizacion(cls, v:int ) -> int:
        #Validar el formato del numero de cotizacion
        if not v or v <= 0 :
            raise ValueError("El numero de cotizacion debe ser mayor a 0")
        return v

    @field_validator("cd_entidad")
    @classmethod
    def validate_entidad(cls, v:int ) -> int:
        #Validar el codigo de entidad
        if v <= 0:
            raise ValueError("El codigo de entidad debe ser mayor a 0")
        return v

class ConsultarPolizaInput(BaseModel):
    cd_entidad: int = Field(
        ...,
        description= "Codigo de entidad de la poliza",
        examples= [1]
    )
    cd_area: int = Field(
        ...,
        description= "Codigo de area de la poliza",
        examples= [1]
    )
    poliza: int = Field(
        ...,
        description= "Numero de poliza de la poliza",
        examples= [12345]
    )
    certificado: int = Field(
        ...,
        description= "Numero de certificado de la poliza",
        examples= [1]
    )
    nu_recibo: Optional[int] = Field(
        default= None,
        description="Numero de recibo (opcional)",
        examples=[1]
    )
    
    @field_validator("cd_entidad", "cd_area", "poliza", "certificado")
    @classmethod
    def validate_positive_int(cls, v: int) -> int:
        #Validar que el valor sea un numero positivo
        if v <= 0:
            raise ValueError("El valor debe ser mayor a 0")
        return v

class MCPResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indica si la operacion fue exitosa"
    )
    data: Optional[dict] = Field(
        default=None,
        description="Datos de la respuesta"
    )
    error: Optional[str] = Field(
        default= None,
        description="Mensaje de error si existe"
    )
    code: Optional[str] = Field(
        default= None,
        description="Codigo de error si existe"
    )