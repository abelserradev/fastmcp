
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