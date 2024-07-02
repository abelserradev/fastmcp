from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Dict
from enum import Enum


class TipoDocumento(Enum):
    VEN = 'VEN'
    PVEN = 'PVEN'
    OPPA = 'OPPA'
    POCD = 'POCD'

class Sexo(Enum):
    M = 'M'
    F = 'F'

class ConsultPersonBase(BaseModel):

    num_documento: str #= Field(..., pattern=r'^[VE]-\d{7,8}$')
    tipo_documento: TipoDocumento



class DocumentoBase(BaseModel):
    tp_documento: TipoDocumento
    nu_documento: str


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
    fe_nacimiento: date
    documento: DocumentoBase
    contacto: ContactoBase

    # @validator('fe_nacimiento')
    # def validate_fecha_nacimiento(cls, v):
    #     if isinstance(v, datetime):
    #         return datetime.strptime(v, '%d/%m/%Y').date()
    #     if isinstance(v, date):
    #         return v.strptime(v, '%d/%m/%Y')
    #     raise ValueError('fecha_nacimiento debe ser un objeto date o datetime')


class CrearPersonaBase(BaseModel):
    persona: PersonaBase
    fe_registro: date

    # @validator('fe_registro')
    # def validate_fecha_registro(cls, v):
    #     if isinstance(v, datetime):
    #         return datetime.strptime(v, '%d/%m/%Y').date()
    #     if isinstance(v, date):
    #         return v.strptime(v, '%d/%m/%Y')
    #     raise ValueError('fe_registro debe ser un objeto date o datetime')



