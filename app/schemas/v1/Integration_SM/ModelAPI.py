from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, validator


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


class ConsultarPersonaBase(BaseModel):
    """
    ConsultarPersonaBase is a data model class used for representing a person's document details.

    Attributes:
        num_documento: A required string field representing the document number. It follows a specific
                       pattern where it starts with a character ('V', 'E', or 'P'), followed by a dash ('-'),
                       and then contains 5 to 30 digits.
    """
    num_documento: str = Field(..., pattern=r"^[VEP]-\d{5,30}$")
    # tipo_documento: TipoDocumento


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


class PersonaBase(BaseModel):
    """
        A class representing a base model for a person.

        Attributes:
            nm_primer_nombre (str): The first name of the person.
            nm_segundo_nombre (str, optional): The middle name of the person. Defaults to None.
            nm_primer_apellido (str): The first surname of the person.
            nm_segundo_apellido (str, optional): The second surname of the person. Defaults to None.
            cd_sexo (Sexo): The gender code of the person.
            fe_nacimiento (Union[datetime, str]): The birth date of the person. Accepts either datetime or str for flexibility.
            documento (DocumentoBase): The document information of the person.
            contacto (ContactoBase): The contact information of the person.

        Methods:
            validate_fecha_nacimiento(cls, v): Validator method for 'fe_nacimiento'. Ensures the date is in the correct format.
    """
    nm_primer_nombre: str
    nm_segundo_nombre: str | None = Field(default=None)
    nm_primer_apellido: str
    nm_segundo_apellido: str | None = Field(default=None)
    cd_sexo: Sexo
    fe_nacimiento: str
    documento: DocumentoBase
    contacto: ContactoBase




class CrearPersonaBase(BaseModel):
    """
        A class used to represent the base structure for creating a persona. It extends from the BaseModel.

        Attributes:
            persona: An instance of PersonaBase, which stores the basic details of a persona.
            fe_registro: A date that can be accepted either as a datetime object or a string in the format 'dd/mm/yyyy'.

        Methods:
            validate_fecha_registro(cls, v):
                Validates and converts the 'fe_registro' attribute. If it is a datetime object, it converts it to a date.
                If it is a string, it attempts to parse it to a date in the 'dd/mm/yyyy' format. Raises a ValueError if the
                input value does not meet the required formats.
    """
    persona: PersonaBase

    fe_registro: Union[
        datetime, str
    ]  # Aceptar tanto datetime como str para mayor flexibilidad

    @validator("fe_registro", pre=True)
    def validate_fecha_registro(cls, v):
        """
        Args:
            v: The value to be validated which can be of type datetime or str.

        Returns:
            A date object parsed from the input datetime or str.

        Raises:
            ValueError: If the input string is not in the format dd/mm/yyyy or if the input is neither a datetime nor a correctly formatted string.
        """
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(
                    v, "%d/%m/%Y"
                ).date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError("fe_registro debe estar en el formato dd/mm/yyyy")
        raise ValueError(
            "fe_registro debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy"
        )


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
    suma_asegurada: Optional[int] = 250




class PersonaPolizaBase(BaseModel):
    """
    This class represents the base model for a policy holder (Persona Poliza) with validation logic.

    Attributes:
        nm_primer_nombre: A string representing the first name.
        nm_primer_apellido: A string representing the last name.
        documento"""
    nm_primer_nombre: str
    nm_primer_apellido: str
    documento: DocumentoBase
    fecha_nacimiento: str


class CrearPolizaBase(BaseModel):
    """
    CrearPolizaBase is a Pydantic model used to create an insurance policy.

    Attributes:
        persona (PersonaPolizaBase): The personal data associated with the policy.
        poliza (PolizaBase): The basic details of the insurance policy.
    """
    persona: PersonaPolizaBase
    poliza: PolizaBase


class EmitirPolizaBase(BaseModel):
    """
    Represents the base model for issuing a policy.

    Attributes:
        cd_entidad (int): Entity code representing the entity issuing the policy.
        nu_cotizacion (int): Quotation number associated with the policy.
    """
    cd_entidad: int
    nu_cotizacion: int


class ConsultarPolizaBase(BaseModel):
    """
    ConsultarPolizaBase represents the base model for querying an insurance policy.

    Attributes:
        cd_entidad (int): The entity code.
        cd_area (int): The area code.
        poliza (int): The policy number.
        certificado (int): The certificate number.
        nu_recibo (int): The receipt number.
    """
    cd_entidad: int
    cd_area: int
    poliza: int
    certificado: int
    nu_recibo: int


class InclusionAnexosPolizaBase(BaseModel):
    cd_entidad: int
    cd_area: int
    nu_poliza: int
    nm_primer_nombre: str
    nm_primer_apellido: str


class ConsultarRecibosPolizaBase(BaseModel):
    cd_entidad: int
    cd_area: int
    poliza: int
    certificado: int


class GetPolizasBase(BaseModel):
    polizas: List[ConsultarRecibosPolizaBase]
