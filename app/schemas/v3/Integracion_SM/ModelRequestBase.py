from datetime import datetime
from enum import Enum
from typing import List, Optional, Union


from pydantic import BaseModel, EmailStr, Field, validator

from app.utils.v1.configs import SUMA_ASEGURADA


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
    CONYUGUE = "CONYUGUE"
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
    """
    A model class representing a base document with specific formatting rules.

    Attributes:
        nu_documento (str): A required string field representing the document number. It follows a specific
                       pattern where it starts with a character ('V', 'E', or 'P'), followed by a dash ('-'),
                       and then contains 5 to 30 digits.
    """
    # tp_documento: TipoDocumento
    nu_documento: str = Field(..., pattern=r"^[VEP]-\d{5,30}$")


class ContactoBase(BaseModel):
    """
        Base class for contact information.

        Attributes:
            nu_area_telefono (str): The area code of the phone number.
            nu_telefono (str): The phone number.
            de_email (EmailStr): The email address.
    """
    nu_area_telefono: str
    nu_telefono: str
    de_email: EmailStr


class Contratante(BaseModel):
    nu_documento_contratante: DocumentoBase
    #tp_documento_contratante: TipoDocumento


class GrupoAsegurado(BaseModel):
    nm_primer_nombre: str
    nm_primer_apellido: str

    fe_nacimiento: str
    nu_documento: str = Field(..., pattern=r"^[VEP]-\d{5,30}$")
    cd_parentesco: Parentesco
    cd_sexo: Sexo

    @validator('fe_nacimiento',pre=True)
    def validate_fecha(cls, v):
        if isinstance(v, str):  # Si es una cadena, validar el formato
            try:
                v_datetime = datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError("La fecha de nacimiento debe estar en el formato dd/mm/yyyy")
            return v
        else:
            raise ValueError("La fecha de nacimiento debe ser una cadena en el formato dd/mm/yyyy")


class PolizaBase(BaseModel):
    """
    PolizaBase class represents a base model for a policy with validation for dates.

    Attributes:
        fe_desde (Union[datetime, str]): The start date of the policy. Accepts both datetime and str formats.
        fe_hasta (Union[datetime, str]): The end date of the policy. Accepts both datetime and str formats.
        frecuencia_cuota (FrecuenciaCuota): The frequency of payment.
        suma_asegurada (Optional[int]): The insured sum. Defaults to 250.

    Methods:
        validate_fe_desde(cls, v):
            Validates and converts the "fe_desde" attribute to a date object if it's a valid datetime or str in %d/%m/%Y format.

        validate_fe_hasta(cls, v):
            Validates and converts the "fe_hasta" attribute to a date object if it's a valid datetime or str in %d/%m/%Y format.
    """
    fe_desde: str
    fe_hasta: str
    frecuencia_cuota: FrecuenciaCuota
    #suma_asegurada: Optional[int] = SUMA_ASEGURADA

    @validator("fe_desde", pre=True)
    def validate_fecha(cls, v):
        if isinstance(v, str):  # Si es una cadena, validar el formato
            try:
                v_datetime = datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError("La fecha de nacimiento debe estar en el formato dd/mm/yyyy")
            return v
        else:
            raise ValueError("La fecha de nacimiento debe ser una cadena en el formato dd/mm/yyyy")


    @validator("fe_hasta", pre=True)
    def validate_fecha(cls, v):
        if isinstance(v, str):  # Si es una cadena, validar el formato
            try:
                v_datetime = datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError("La fecha de nacimiento debe estar en el formato dd/mm/yyyy")
            return v
        else:
            raise ValueError("La fecha de nacimiento debe ser una cadena en el formato dd/mm/yyyy")


class Titular(BaseModel):
    nm_primer_nombre: str
    nm_primer_apellido: str

    fe_nacimiento: str
    nu_documento: Optional[DocumentoBase]
    cd_sexo: Sexo

    @validator('fe_nacimiento',pre=True)
    def validate_fecha(cls, v):
        if isinstance(v, str):  # Si es una cadena, validar el formato
            try:
                v_datetime = datetime.strptime(v, '%d/%m/%Y')
            except ValueError:
                raise ValueError("La fecha de nacimiento debe estar en el formato dd/mm/yyyy")
            return v
        else:
            raise ValueError("La fecha de nacimiento debe ser una cadena en el formato dd/mm/yyyy")


class Cotizacion(BaseModel):
    poliza: PolizaBase
    contratante: Contratante
    grupoAsegurados: Optional[List[GrupoAsegurado]]
    titular: Titular

