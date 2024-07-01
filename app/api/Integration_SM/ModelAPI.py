from pydantic import BaseModel, Field
from typing import List, Dict
from enum import Enum


class TipoDocumento(Enum):
    VEN = 'VEN'
    PVEN = 'PVEN'
    OPPA = 'OPPA'
    POCD = 'POCD'

class ConsultPersonBase(BaseModel):
    num_documento: str = Field(..., pattern=r'^[VE]-\d{7,8}$')
    tipo_documento: TipoDocumento
