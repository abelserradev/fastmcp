import json

from fastapi import APIRouter
import requests

from app.api.Integration_SM.ModelAPI import ConsultPersonBase
from app.middlewares.verify_api_key import APIKeyVerifier
from app.utils.LoggerSingleton import logger
from app.utils.configs import (
    SM_ENDPOINT,
    SM_PRIMARY_KEY,
    SM_SECONDARY_KEY,
    API_KEY_AUTH,
    USER,
    APPLICATION, SUBSCRIPTION_KEY
)

router = APIRouter(
    tags=["SM"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)

url_consult_person = f"{SM_ENDPOINT}/consultarpersona"

headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}


@router.post("/consultar_persona", summary="Consultar persona en Seguros Mercantil")
def consultar_persona(request: ConsultPersonBase) -> dict:

    tp_document = request.tipo_documento.value
    num_document = request.num_documento


    body = json.dumps({
        "aplicacion": APPLICATION,
        "funcionalidad": "CONSULTAR_PERSONA_V",
        "usuario": USER,
        "persona": {
            "tp_documento": tp_document,
            "nu_documento": num_document
        }
    })

    logger.info(f"body: {body}")
    logger.info(f"headers: {headers}")
    logger.info(f"url_consult_person: {url_consult_person}")
    response = requests.post(url_consult_person, data=body, headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)

    # verificar si el request fue exitoso
    if response.status_code == 200:
        return {"status": "success", "data": response_json}

    return {"status": "error", "data": response_json}

