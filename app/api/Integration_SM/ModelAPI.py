from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Dict, Union
from enum import Enum


class TipoDocumento(Enum):
    VEN = 'VEN'
    PVEN = 'PVEN'
    OPPA = 'OPPA'
    POCD = 'POCD'

class Sexo(Enum):
    M = 'M'
    F = 'F'

class ConsultarPersonaBase(BaseModel):

    num_documento: str = Field(..., pattern=r'^[VEP]-\d{7,8}$')
    #tipo_documento: TipoDocumento



class DocumentoBase(BaseModel):
    #tp_documento: TipoDocumento
    nu_documento: str = Field(..., pattern=r'^[VEP]-\d{7,20}$')


class ContactoBase(BaseModel):
    nu_area_telefono: str
    nu_telefono: str
    de_email: EmailStr


class PersonaBase(BaseModel):
    nm_primer_nombre: str
    nm_segundo_nombre: str | None = Field(default=None)
    nm_primer_apellido: str
    nm_segundo_apellido: str | None = Field(default=None)
    cd_sexo: Sexo
    fe_nacimiento: Union[datetime, str]  # Aceptar tanto datetime como str para mayor flexibilidad
    documento: DocumentoBase
    contacto: ContactoBase



    @validator('fe_nacimiento', pre=True)
    def validate_fecha_nacimiento(cls, v):
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError('fe_nacimiento debe estar en el formato dd/mm/yyyy')
        raise ValueError('fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy')


class CrearPersonaBase(BaseModel):
    persona: PersonaBase

    fe_registro: Union[datetime, str]  # Aceptar tanto datetime como str para mayor flexibilidad

    @validator('fe_registro', pre=True)
    def validate_fecha_registro(cls, v):
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError('fe_registro debe estar en el formato dd/mm/yyyy')
        raise ValueError('fe_registro debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy')


class FrecuenciaCuota(Enum):
    MENSUAL = 'MENSUAL'
    TRIMESTRAL = 'TRIMESTRAL'
    SEMESTRAL = 'SEMESTRAL'
    ANUAL = 'ANUAL'


class PolizaBase(BaseModel):
    fe_desde: Union[datetime, str]  # Aceptar tanto datetime como str
    fe_hasta: Union[datetime, str]  # Aceptar tanto datetime como str
    frecuencia_cuota: FrecuenciaCuota
    suma_asegurada: float

    @validator('fe_desde', pre=True)
    def validate_fe_desde(cls, v):
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError('fe_nacimiento debe estar en el formato dd/mm/yyyy')
        raise ValueError('fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy')

    @validator('fe_hasta', pre=True)
    def validate_fe_hasta(cls, v):
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError('fe_nacimiento debe estar en el formato dd/mm/yyyy')
        raise ValueError('fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy')


class PersonaPolizaBase(BaseModel):
    nm_primer_nombre: str
    nm_primer_apellido: str
    documento: DocumentoBase
    fecha_nacimiento: Union[datetime, str]  # Aceptar tanto datetime como str para

    @validator('fecha_nacimiento', pre=True)
    def validate_fecha_nacimiento(cls, v):
        if isinstance(v, datetime):
            return v.date()  # Si es datetime, convertir a date
        elif isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()  # Intentar parsear el str a date
            except ValueError:
                raise ValueError('fe_nacimiento debe estar en el formato dd/mm/yyyy')
        raise ValueError('fe_nacimiento debe ser un objeto datetime o una cadena en el formato dd/mm/yyyy')


class CrearPolizaBase(BaseModel):
    persona: PersonaPolizaBase
    poliza: PolizaBase


class EmitirPolizaBase(BaseModel):
    cd_entidad: int
    nu_cotizacion: int

