import json

from fastapi import APIRouter, Security, HTTPException
import requests

from app.api.Integration_SM.ModelAPI import ConsultarPersonaBase, CrearPersonaBase, CrearPolizaBase
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
from app.utils.constants import (
    payload_persona,
    tipo_documento,
    payload_cotizacion,
    frecuencia_cuota,
    fields_setup
)

router = APIRouter(
    tags=["SM"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)

url_consult_persona = f"{SM_ENDPOINT}/consultarpersona"
url_crear_persona = f"{SM_ENDPOINT}/crearpersona"

headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}


@router.post("/consultar_persona", summary="Consultar persona en Seguros Mercantil")
def consultar_persona(request: ConsultarPersonaBase, api_key: str = Security(api_key_verifier)) -> dict:
    num_document = request.dict(exclude_unset=True)["num_documento"]

    tp_document = tipo_documento[num_document[0]]
    num_document = num_document[2:] if num_document[0] == "P" else num_document

    body = {
        "aplicacion": APPLICATION,
        "funcionalidad": "CONSULTAR_PERSONA_V",
        "usuario": USER,
        "persona": {
            "tp_documento": tp_document,
            "nu_documento": num_document
        }
    }

    logger.info(f"body: {body}")
    logger.info(f"headers: {headers}")
    logger.info(f"url_consult_persona: {url_consult_persona}")

    response = requests.post(url_consult_persona, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)

    # verificar si el request fue exitoso
    if response.status_code == 200:
        return {"status": "success", "data": response_json}

    return {"status": "error", "data": response_json}


@router.post("/crear_persona", summary="Crear persona en Seguros Mercantil")
def crear_persona(request: CrearPersonaBase, api_key: str = Security(api_key_verifier)) -> dict:
    data = request.dict(exclude_unset=True)
    logger.info(f"data: {data}")
    body = payload_persona.copy()
    nu_documento = data["persona"]["documento"]["nu_documento"][2:] if data["persona"]["documento"]["nu_documento"][0] == "P" else data["persona"]["documento"]["nu_documento"]
    tp_documento = tipo_documento[data["persona"]["documento"]["nu_documento"][0]]

    fe_nacimiento = data["persona"]["fe_nacimiento"].strftime("%d/%m/%Y")
    fe_registro = data["fe_registro"].strftime("%d/%m/%Y")
    body["persona"][0]["nm_primer_nombre"] = data["persona"]["nm_primer_nombre"]
    body["persona"][0]["nm_primer_apellido"] = data["persona"]["nm_primer_apellido"]
    body["persona"][0]["cd_sexo"] = data["persona"]["cd_sexo"].value
    body["persona"][0]["fe_nacimiento"] = fe_nacimiento
    body["persona"][0]["fe_registro"] = fe_registro
    body["persona"][0]["persona_email"][0]["de_email"] = data["persona"]["contacto"]["de_email"]
    body["persona"][0]["persona_telefono"][0]["nu_area"] = data["persona"]["contacto"]["nu_area_telefono"]
    body["persona"][0]["persona_telefono"][0]["nu_telefono"] = data["persona"]["contacto"]["nu_telefono"]
    body["persona"][0]["nu_documento"] = nu_documento
    body["persona"][0]["tp_documento"] = tp_documento
    body["persona"][0]["nu_documento_seccion2"] = nu_documento[2:]
    body["persona"][0]["nu_documento_seccion1"] = nu_documento[:1]
    body["persona"][0]["cd_nacionalidad"] = "VEN"
    body["persona"][0]["cd_pais_nacimiento"] = "VEN"
    logger.info(f"body: {json.dumps(body)}")
    logger.info(f"headers: {headers}")
    logger.info(f"url_crear_persona: {url_crear_persona}")

    response = requests.post(url_crear_persona, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)

    # verificar si el request fue exitoso
    if response.status_code == 200:
        return {"status": "success", "data": response_json}

    return {"status": "error", "data": response_json}


@router.post("/crear_poliza", summary="Crear poliza de persona en Seguros Mercantil")
def crear_poliza(request: CrearPolizaBase, api_key: str = Security(api_key_verifier)) -> dict:

    data = request.dict(exclude_unset=True)
    fecha_nacimiento = data["persona"]["fecha_nacimiento"].strftime("%d-%m-%Y")
    suma_poliza = data["poliza"]["suma_asegurada"]
    fe_desde = data["poliza"]["fe_desde"].strftime("%d/%m/%Y")
    fe_hasta = data["poliza"]["fe_hasta"].strftime("%d/%m/%Y")
    cd_plan_pago = frecuencia_cuota[data["poliza"]["frecuencia_cuota"].value]
    nu_documento = data["persona"]["documento"]["nu_documento"][2:] if data["persona"]["documento"]["nu_documento"][0] == "P" else data["persona"]["documento"]["nu_documento"]
    tp_documento = tipo_documento[data["persona"]["documento"]["nu_documento"][0]]
    fullname = f"{data['persona']['nm_primer_nombre']} {data['persona']['nm_primer_apellido']}"

    body = payload_cotizacion.copy()
    body["coll_bienes"]["bienes"][0]["de_bien"] = fullname

    body["coll_generales"]["generales"][0]["fe_desde"] = fe_desde
    body["coll_generales"]["generales"][0]["fe_hasta"] = fe_hasta
    body["coll_generales"]["generales"][0]["cd_plan_pago"] = cd_plan_pago
    body["coll_generales"]["generales"][0]["nm_cliente"] = fullname
    body["coll_generales"]["generales"][0]["nu_documento"] = nu_documento
    body["coll_generales"]["generales"][0]["tp_documento"] = tp_documento
    body["coll_generales"]["generales"][0]["nu_documento_contratante"] = nu_documento
    body["coll_generales"]["generales"][0]["tp_documento_contratante"] = tp_documento

    coll_datos = {"datos":[]}
    for item in body["coll_datos"]["datos"]:
        if item["cd_dato"] == 990150:
            item["valor"] = suma_poliza
        if item["cd_dato"] == 990160:
            item["valor"] = fecha_nacimiento
        coll_datos["datos"].append(item)

    body["coll_datos"] = coll_datos
    logger.info(f"data: {body}")

    response = requests.post(url_crear_persona, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)

    # verificar si el request fue exitoso
    if response.status_code == 200:
        return {"status": "success", "data": response_json}

    return {"status": "error", "data": response_json}
