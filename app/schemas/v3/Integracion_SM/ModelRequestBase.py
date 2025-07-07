from datetime import datetime
from enum import Enum
from typing import List, Optional, Union


from pydantic import BaseModel, Field

from app.utils.v1.regular_expressions import expr_num_documento


class TipoDocumento(Enum):
    """
        Enum class representing different types of documents.

        Attributes:
          VEN: Represents a 'VEN' document.
          PVEN: Represents a 'PVEN' document.
          OPPA: Represents an 'OPPA' document.
          POCD: Represents a 'POCD' document.
        """
    VEN = "VEN"
    PVEN = "PVEN"
    OPPA = "OPPA"
    POCD = "POCD"


class Sexo(Enum):
    """
    An enumeration representing the binary sexes.

    Attributes:
      M: Represents male sex.
      F: Represents female sex.
    """
    M = "M"
    F = "F"


class Parentesco(Enum):
    CONYUGE = "CONYUGE"
    HIJO = "HIJO"
    PADRE = "PADRE"
    MADRE = "MADRE"
    OTROS = "OTROS"


class FrecuenciaCuota(Enum):
    """
    Enum class representing the frequency of quotas.

    Attributes:
        MENSUAL: Monthly frequency.
        TRIMESTRAL: Quarterly frequency.
        SEMESTRAL: Semi-annual frequency.
        ANUAL: Annual frequency.
    """
    MENSUAL = "MENSUAL"
    TRIMESTRAL = "TRIMESTRAL"
    SEMESTRAL = "SEMESTRAL"
    ANUAL = "ANUAL"



class DocumentoBase(BaseModel):
    nu_documento: str = Field(..., pattern=expr_num_documento)


class PolizaBase(BaseModel):
    fe_desde: Union[datetime, str]  # Aceptar tanto datetime como str
    fe_hasta: Union[datetime, str]  # Aceptar tanto datetime como str
    frecuencia_cuota: FrecuenciaCuota
    #suma_asegurada: Optional[int] = 250


class PersonaPolizaBase(BaseModel):

    nm_primer_nombre: str
    nm_primer_apellido: str
    documento: DocumentoBase
    fecha_nacimiento: str
    sexo: Sexo


class BeneficiariosBase(BaseModel):
    cd_parentesco: Parentesco
    nu_documento: str = Field(..., pattern=expr_num_documento)
    fe_nacimiento: str
    nm_primer_nombre: str
    cd_sexo: Sexo
    nm_primer_apellido: str



class CrearPolizaBase(BaseModel):
    """
    CrearPolizaBase is a Pydantic model used to create an insurance policy.

    Attributes:
        persona (PersonaPolizaBase): The personal data associated with the policy.
        poliza (PolizaBase): The basic details of the insurance policy.
    """
    persona: PersonaPolizaBase
    poliza: PolizaBase
    tiene_conyuge: Optional[bool] = False
    cantidad_hijos: Optional[int] = 0
    tiene_padre: Optional[bool] = False
    tiene_madre: Optional[bool] = False
    beneficiarios: Optional[List[BeneficiariosBase]] = []


class DatosPolizaBase(BaseModel):
    cd_entidad: int
    cd_area: int
    nu_poliza: int
    nu_certificado: int
    nu_endoso: int

