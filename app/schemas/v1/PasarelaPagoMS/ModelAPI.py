from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, ClassVar
import re

from pydantic import BaseModel, EmailStr, Field, field_validator


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
    fe_nacimiento: Union[datetime, str]  # Aceptar tanto datetime como str para mayor flexibilidad
    documento: DocumentoBase
    contacto: ContactoBase

    @field_validator("fe_nacimiento")
    def validate_fecha_nacimiento(cls, v):
        """
        Args:
            v: The value to be validated and possibly converted.

        Returns:
            The date object parsed from the input value.

        Raises:
            ValueError: If the input value is a string that cannot be parsed to a date in the format dd/mm/yyyy, or if the input is neither a datetime object nor a properly formatted string.
        """
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                date_formated = datetime.strptime(
                    v, "%d/%m/%Y"
                ).date()  # Intentar parsear el str a date
                return date_formated.strftime("%d/%m/%Y")
            except ValueError:
                raise ValueError("fe_nacimiento debe estar en el formato dd/mm/yyyy")
        raise ValueError(
            "fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy"
        )




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

    fe_registro: str # Aceptar tanto datetime como str para mayor flexibilidad

    @field_validator("fe_registro")
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
                date_formated = datetime.strptime(
                    v, "%d/%m/%Y"
                ).date()  # Intentar parsear el str a date
                return date_formated.strftime("%d/%m/%Y")
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
    fe_desde: Union[datetime, str]  # Aceptar tanto datetime como str
    fe_hasta: Union[datetime, str]  # Aceptar tanto datetime como str
    frecuencia_cuota: FrecuenciaCuota
    suma_asegurada: Optional[int] = 250

    @field_validator("fe_desde")
    def validate_fe_desde(cls, v):
        """
        Args:
            v: The value to be validated and converted. It can be a datetime object or a string in the format dd/mm/yyyy.

        Returns:
            date: The extracted date from a datetime object or the parsed date from a string.

        Raises:
            ValueError: If the provided value is not a datetime object or a properly formatted string.
        """
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(
                    v, "%d/%m/%Y"
                ).date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError("fe_nacimiento debe estar en el formato dd/mm/yyyy")
        raise ValueError(
            "fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy"
        )

    @field_validator("fe_hasta")
    def validate_fe_hasta(cls, v):
        """
        Args:
            v: The input value that needs to be validated. It can either be a datetime object or a string in the format dd/mm/yyyy.

        Returns:
            A date object if the input is valid.

        Raises:
            ValueError: If the input is a string and cannot be parsed as a date in the format dd/mm/yyyy.
            ValueError: If the input is neither a datetime object nor a string formatted as dd/mm/yyyy.
        """
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(
                    v, "%d/%m/%Y"
                ).date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError("fe_nacimiento debe estar en el formato dd/mm/yyyy")
        raise ValueError(
            "fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy"
        )



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
    fecha_nacimiento: Union[datetime, str]  # Aceptar tanto datetime como str para

    @field_validator("fecha_nacimiento")
    def validate_fecha_nacimiento(cls, v):
        """
        Args:
            v: The input value to validate. It can be a datetime object or a string representing a date in the format "dd/mm/yyyy".

        Returns:
            A date object converted from the input datetime or parsed from the input string.

        Raises:
            ValueError: If the input string cannot be parsed to a date or if the input is neither a datetime object nor a correctly formatted string.
        """
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(
                    v, "%d/%m/%Y"
                ).date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError("fe_nacimiento debe estar en el formato dd/mm/yyyy")
        raise ValueError(
            "fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy"
        )


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
    nu_recibo: Optional[int] = 0


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


class MonedaPagoEnum(Enum):
    BS = "BS"
    USD = "USD"

class TipoInstrumentoPagoEnum(Enum):
    C2P = "C2P"
    TDD = "TDD"
    TDC = "TDC"




class InstrumentoC2PBase(BaseModel):

    numero: int
    tp_identidad: str = Field(..., pattern=r"^[VE]$")
    doc_identidad: str = Field(..., pattern=r"\d{5,30}$")
    nu_telefono: str = Field(...,
                             pattern=r"^58(412|414|416|424|426)\d{7}$",
                             description="Número de teléfono debe iniciar con 58 y contener un prefijo válido, seguido de 7 dígitos.")
    cd_banco: str = Field(..., pattern=r"^(0102|0104|0105|0108|0114|0115|0116|0128|0134|0137|0138|0146|0156|0157|0163|0166|0168|0169|0171|0173|0174|0175|0177|0191)$")
    otp: str

class InstrumentoTDCBase(BaseModel):

    numero: int
    fe_vencimiento: str = Field(..., pattern=r"^(0[1-9]|1[0-2])-\d{4}$")
    cd_verificacion: int
    nombre_tarjeta: str
    tp_identidad: str = Field(..., pattern=r"^[VE]$")
    doc_identidad: str = Field(..., pattern=r"\d{5,30}$")

class TPCuentaEnum(Enum):
    CC = "CC"
    CA = "CA"

class InstrumentoTDDBase(BaseModel):

    numero: int
    fe_vencimiento: str = Field(..., pattern=r"^(0[1-9]|1[0-2])-\d{4}$")
    cd_verificacion: int
    nombre_tarjeta: str
    tp_identidad: str = Field(..., pattern=r"^[VE]$")
    doc_identidad: str = Field(..., pattern=r"\d{5,30}$")
    tp_cuenta: TPCuentaEnum
    otp: str



class InstrumentoPagoBase(BaseModel):
    instrumento_tdd: Optional[InstrumentoTDDBase] = None
    instrumento_tdc: Optional[InstrumentoTDCBase] = None
    instrumento_c2p: Optional[InstrumentoC2PBase] = None

class PagoBase(BaseModel):
    moneda_pago: MonedaPagoEnum
    tipo_instrumento_pago: TipoInstrumentoPagoEnum
    instrumento_pago: InstrumentoPagoBase


class ReciboPagoBase(BaseModel):
    cd_entidad: int
    cd_area: int
    nu_poliza: int
    nu_certificado: int
    cd_recibo: int
    nu_convenio_pago: int
    nu_cuota: int

class RegistroPagoBase(BaseModel):
    recibo_poliza_pago: ReciboPagoBase
    pago: PagoBase

class InstrumentoC2PMnuEnum(Enum):
    C2P = "C2P"
    TDD = "TDD"

class InstrumentoModel(BaseModel):
    tp_identidad: str = Field(..., pattern=r"^[VE]$", description="Cédula de identidad comienza con V o E, de venezolano o extranjero")
    doc_identidad: str = Field(..., pattern=r"\d{5,10}$", description="Cédula puede ser entre 5 a 10 dígitos de longitud.")
    nu_telefono: str = Field(...,
                             pattern=r"^58(412|414|416|424|426)\d{7}$",
                             description="Número de teléfono debe iniciar con 58 y contener un prefijo válido, seguido de 7 dígitos.")


class OtpMbuBase(BaseModel):
    tipo_instrumento: InstrumentoC2PMnuEnum
    instrumento: InstrumentoModel

class TasaBCVBase(BaseModel):
    fe_tasa: str

    # Definimos un patrón de regex para validar el formato dd/mm/yyyy
    fecha_regex: ClassVar[re.Pattern] = re.compile(r'^\d{2}/\d{2}/\d{4}$')

    @field_validator('fe_tasa')
    def validate_fe_tasa(cls, value):
        if not cls.fecha_regex.match(value):
            raise ValueError('El formato de fe_tasa debe ser dd/mm/yyyy')
        return value


class PolizaReciboCuotaBase(BaseModel):
    cd_entidad: Optional[str] = "1"
    cd_area: Optional[str] ="71"
    nu_poliza: str
    nu_certificado: Optional[str] = "1"
    cd_recibo: str
    nu_convenio_pago: str
    nu_cuota: Optional[str] = "1"




class TipoPagoEnum(Enum):
    USD = "USD"
    BS = "BS"


class PagoBase(BaseModel):
    moneda_pago: TipoPagoEnum
    moneda_recibo: Optional[str] = None
    monto_recibo: Optional[str] = None
    monto_pago: str
    cd_aprobacion: str
    tasa_cambio: Optional[str] = None

    # Ejemplo de serialización que excluye campos con valor None:
    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)




class NotificacionPagoBase(BaseModel):
    poliza_recibo_cuota: List[PolizaReciboCuotaBase]
    tipo_instrumento_pago: Optional[str] = ""
    nombre_pagador: str
    tipo_pago: TipoPagoEnum
    notificacion_pago: PagoBase