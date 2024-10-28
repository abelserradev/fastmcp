from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class TipoDocumento(Enum):
    """
    Enumeration representing different types of documents.

    Attributes:
        VEN: Represents a "VEN" type document.
        PVEN: Represents a "PVEN" type document.
        OPPA: Represents an "OPPA" type document.
        POCD: Represents a "POCD" type document.
    """
    VEN = "VEN"
    PVEN = "PVEN"
    OPPA = "OPPA"
    POCD = "POCD"


class Sexo(Enum):
    """
    Enum representing gender categories.

    Attributes:
        M: String value "M", representing male gender.
        F: String value "F", representing female gender.
    """
    M = "M"
    F = "F"



class CoberturaResponse(BaseModel):

    cd_garantia: int
    de_garantia: str
    suma: int
    prima: Union[float, int]
    comision: int
    total_prima_bien: Union[float, int]


class BienesResponse(BaseModel):

    nu_bien: int
    de_bien: str
    coberturas: List[CoberturaResponse]


class CotizacionResponse(BaseModel):
    nu_cotizacion: int
    cd_entidad: int
    nu_item: int
    cd_plan: int
    de_plan: str
    cd_moneda: int
    mt_suma: Union[int,float]
    mt_prima_total: Union[int,float]
    cd_plan_pago: int
    de_plan_pago: str
    nu_total_cuota: int
    mt_prima_pago: Union[int,float]
    in_seleccion: str
    mt_sig_cuota: Union[int,float]
    nu_sec_estructura: str
    cd_agente_bancario: str
    nm_agente_bancario: str
    bienes: List[BienesResponse]


class StatusResponseCuadroPoliza(BaseModel):
    code: str
    descripcion: str

class CuadroPolizaResponse(BaseModel):
    status: StatusResponseCuadroPoliza
    reporte_codificado: str