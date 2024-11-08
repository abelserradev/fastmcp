import json

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status


from app.middlewares.verify_api_key import APIKeyVerifier
from app.schemas.WebHookZoho.ModelRequest import PayloadRequest
from app.utils.v1.AsyncHttpx import get_client, fetch_url
from app.utils.v1.configs import API_KEY_AUTH, URL_API_ZOHO

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



@router.post(
    "/prueba",
    status_code=status.HTTP_200_OK,
    summary="Prueba Zoho",
)
async def webhook_insurances(request: PayloadRequest):
    payload = request.model_dump()["payload"]
    logger.info(f"Payload: {payload}")

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
