import httpx
from dataclasses import dataclass

from app.utils.v2.LoggerSingletonDB import logger
from fastapi import HTTPException, status


@dataclass
class ResponseAnularPoliza:
    message: str
    status_code: int
    descripcion: str
    code: str

def request_anular_poliza(url: str, data: dict, headers: dict)-> ResponseAnularPoliza:

    response = httpx.post(url, headers=headers, json=data)
    result = response.json()

    return ResponseAnularPoliza(
        message=result["response"]["message"],
        status_code=response.status_code,
        descripcion=result["status"]["descripcion"],
        code=result["status"]["code"]
    )
