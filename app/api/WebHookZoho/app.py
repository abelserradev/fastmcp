import json

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status


from app.middlewares.verify_api_key import APIKeyVerifier
from app.utils.v1.AsyncHttpx import get_client, fetch_url
from app.utils.v1.configs import API_KEY_AUTH

from app.utils.v1.LoggerSingleton import logger


router = APIRouter(
    tags=["WebHook Zoho CRM v1"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
}

payload = {
    "first_name": "Blanca",
    "last_name": "Esperanza",
    "CustomerId": "672b7c18bc0da02bc9851d50",
    "nu_poliza": "173016",
    "Frecuencia": "Mensual",
    "Status": "pendiente",
    "fecha_nac": "1934-12-31",
    "ambiente": "Desarrollo",
    "ciudad": "Caracas",
    "correo": "glenis62@asistensi.com",
    "phone_one": "+584121111162",
    "canal": "web",
    "montoplan": "40",
    "sexo": "Masculino",
    "dni": "V2100162",
    "pregunta": "Si",
    "phone_one_contact": "+584121111162",
    "city_contact": "Caracas",
    "email_contact": "glenis62@asistensi.com",
    "fe_desde_cert": "06/11/2024",
    "fe_hasta_cert": "06/11/2025"
}

URL_API_ZOHO="https://flow.zoho.com/740897154/flow/webhook/incoming?zapikey=1001.dd14287df51ed2810b6542e3858806ac.b43bd12d9cbe2a2a65b78b9049f5a737&isdebug=false"



@router.get(
    "/prueba",
    status_code=status.HTTP_200_OK,
    summary="Prueba Zoho",
)
async def webhook_insurances() -> dict:
    client = httpx.Client()
    resp = client.post(URL_API_ZOHO, json=payload, headers=headers, timeout=180)
    if resp.status_code == 200:
        logger.info("Webhook enviado correctamente")
        return {"message": "Webhook enviado correctamente"}
    else:
        logger.error("Error al enviar el webhook")
        raise HTTPException(
            status_code=resp.status_code, detail="Error al enviar el webhook"
        )
