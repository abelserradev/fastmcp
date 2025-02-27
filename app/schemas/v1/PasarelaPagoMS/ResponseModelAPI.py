
from enum import Enum
from typing import List

from pydantic import BaseModel

from app.schemas.v1.PasarelaPagoMS.ModelAPI import ReciboPagoBase


class PolizaReciboCuotaResponseBase(ReciboPagoBase):
    nu_ingreso_caja: str

class ResponsePagoBase(BaseModel):
    orden_comercio: int
    cd_aprobacion: int
    poliza_recibo_cuota: List[PolizaReciboCuotaResponseBase]


class ResponseOTPMBU(BaseModel):
    fecha_procesamiento: str
    estatus: str
    min_expiracion: str

class ResponseTasaBCV(BaseModel):
    in_tasa: int
    tasa_compra: float
    cd_moneda: int
    tasa_venta: float
    cd_producto: int
    fe_tasa: str