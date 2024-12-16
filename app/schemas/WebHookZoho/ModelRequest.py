from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, validator, field_validator





class PayloadModel(BaseModel):
    first_name: str
    last_name: str
    CustomerId: str
    nu_poliza: str
    Frecuencia: str
    Status: str
    fecha_nac: str
    ambiente: str
    ciudad: str
    correo: str
    phone_one: str
    canal: str
    montoplan: str
    sexo: str
    dni: str
    pregunta: str
    phone_one_contact: str
    city_contact: str
    email_contact: str
    fe_desde_cert: str
    fe_hasta_cert: str

class PayloadRequest(BaseModel):
    payload: PayloadModel