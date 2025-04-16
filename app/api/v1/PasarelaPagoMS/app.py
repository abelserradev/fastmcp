import json
from typing import Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.middlewares.verify_api_key import APIKeyVerifier
from app.schemas.v1.PasarelaPagoMS.ModelAPI import (
    RegistroPagoBase,
    OtpMbuBase,
    TasaBCVBase,
    NotificacionPagoBase,
)
from app.schemas.v1.PasarelaPagoMS.ResponseModelAPI import ResponsePagoBase, ResponseOTPMBU, ResponseTasaBCV
from app.utils.v1.AsyncHttpx import get_client, fetch_url
from app.utils.v1.configs import API_KEY_AUTH, MID, MOCKUP
from app.utils.v1.constants import (url_registrar_pago,
                                    headers_pasarela_ms, url_otp_mbu, headers_suscripcion_ms, url_suscripcion_tasa_bcv,
                                    url_notificacion_pago
                                    )
from app.utils.v1.LoggerSingleton import logger
from app.utils.v2.SyncHttpx import sync_fetch_url
from app.utils.v2.payload_templates import payload_pasarela_pago, payload_pasarela_otp, payload_tasa_bcv, \
    payload_notificacion_pago
from datetime import datetime
router = APIRouter(
    tags=["Pasarela Pago MS Version 1"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


@router.post(
    "/registrar_pago",
    #response_model=ResponsePagoBase,
    status_code=status.HTTP_200_OK,
    summary="Registrar Pago Pasarela MS",
)
def registrar_pago(
    request: RegistroPagoBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
):

    data = request.model_dump()
    logger.info(f"Data: {data}")

    recibo_poliza_pago = data.get("recibo_poliza_pago")
    pago = data.get("pago")

    moneda_pago = pago.get("moneda_pago").value
    instrumento_pago = pago.get("instrumento_pago")
    tipo_instrumento_pago = pago.get("tipo_instrumento_pago").value

    instrumento = {}
    match tipo_instrumento_pago:
        case "C2P":
            instrumento_c2p = instrumento_pago.get("instrumento_c2p")
            instrumento["numero"] = instrumento_c2p.get("numero")
            instrumento["tp_identidad"] = instrumento_c2p.get("tp_identidad")
            instrumento["doc_identidad"] = instrumento_c2p.get("doc_identidad")
            instrumento["nu_telefono"] = instrumento_c2p.get("nu_telefono")
            instrumento["cd_banco"] = instrumento_c2p.get("cd_banco")
            instrumento["otp"] = instrumento_c2p.get("otp")
        case "TDD":
            instrumento_tdd = instrumento_pago.get("instrumento_tdd")
            instrumento["numero"] = instrumento_tdd.get("numero")
            instrumento["fe_vencimiento"] = instrumento_tdd.get("fe_vencimiento")
            instrumento["cd_verificacion"] = instrumento_tdd.get("cd_verificacion")
            instrumento["nombre_tarjeta"] = instrumento_tdd.get("nombre_tarjeta")
            instrumento["tp_identidad"] = instrumento_tdd.get("tp_identidad")
            instrumento["doc_identidad"] = instrumento_tdd.get("doc_identidad")
            instrumento["tp_cuenta"] = instrumento_tdd.get("tp_cuenta").value
            instrumento["otp"] = instrumento_tdd.get("otp")
        case "TDC":
            instrumento_tdc = instrumento_pago.get("instrumento_tdc")
            instrumento["numero"] = instrumento_tdc.get("numero")
            instrumento["fe_vencimiento"] = instrumento_tdc.get("fe_vencimiento")
            instrumento["cd_verificacion"] = instrumento_tdc.get("cd_verificacion")
            instrumento["nombre_tarjeta"] = instrumento_tdc.get("nombre_tarjeta")
            instrumento["tp_identidad"] = instrumento_tdc.get("tp_identidad")
            instrumento["doc_identidad"] = instrumento_tdc.get("doc_identidad")
        case _:
            raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error tipo de instrumento de pago: {tipo_instrumento_pago}",
                    )

    logger.info(f"Recibo poliza pago:{recibo_poliza_pago}")
    logger.info(f"Moneda: {moneda_pago}")
    logger.info(f"Tipo de instrumento de pago:{tipo_instrumento_pago}")
    logger.info(f"Instrumento de pago: {instrumento}")
    payload_pasarela_pago["datos"]["poliza_recibo_cuota"] = [recibo_poliza_pago]
    payload_pasarela_pago["datos"]["tipo_instrumento_pago"] = tipo_instrumento_pago
    payload_pasarela_pago["datos"]["moneda_pago"] = moneda_pago
    match tipo_instrumento_pago:
        case "TDD":
            tipo_instrumento = "instrumento_tdd"
            if "instrumento_tdc" in payload_pasarela_pago["datos"].keys():
                del payload_pasarela_pago["datos"]["instrumento_tdc"]
            if "instrumento_c2p" in payload_pasarela_pago["datos"].keys():
                del payload_pasarela_pago["datos"]["instrumento_c2p"]
        case "C2P":
            tipo_instrumento = "instrumento_c2p"
            if "instrumento_tdc" in payload_pasarela_pago["datos"].keys():
                del payload_pasarela_pago["datos"]["instrumento_tdc"]
            if "instrumento_tdd" in payload_pasarela_pago["datos"].keys():
                del payload_pasarela_pago["datos"]["instrumento_tdd"]
        case "TDC":
            tipo_instrumento = "instrumento_tdc"
            if "instrumento_tdd" in payload_pasarela_pago["datos"].keys():
                del payload_pasarela_pago["datos"]["instrumento_tdd"]
            if "instrumento_c2p" in payload_pasarela_pago["datos"].keys():
                del payload_pasarela_pago["datos"]["instrumento_c2p"]
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Tipo de instrumento no es C2P,TDC o TDD")

    payload_pasarela_pago["datos"][tipo_instrumento] = instrumento



    try:
        logger.info(f"URL:{url_registrar_pago}")
        logger.info(f"HEADER: {headers_pasarela_ms}")
        logger.info(f"Payload: {json.dumps(payload_pasarela_pago)}")
        http_client = httpx.Client(verify=False)
        response = http_client.post(
            url_registrar_pago,
            headers=headers_pasarela_ms,
            json=payload_pasarela_pago,
            timeout=None
        )
    except httpx.RequestError as e:
        logger.error(f"Error en la solicitud: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )
    except httpx.ReadTimeout as e:
        logger.error(f"Tiempo de espera excedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Tiempo de espera excedido",
        )
    except httpx.HTTPError as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )



    if response.status_code != 200:

        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":

        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")


    # # Convierte la respuesta en JSON
    response_json = response.json()
    result = response_json.get("datos")
    return result




@router.post(
    "/otp_mbu",
    response_model=ResponseOTPMBU,
    status_code=status.HTTP_200_OK,
    summary="Registrar Pago Pasarela MS",
)
def otp_mbu(
    request: OtpMbuBase,
    #client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
):
    data = request.model_dump()
    logger.info(f"Data: {data}")
    tipo_instrumento = data.get("tipo_instrumento").value

    instrumento = data.get("instrumento")
    payload = payload_pasarela_otp.copy()
    payload["datos"]["tipo_instrumento"] = tipo_instrumento

    match tipo_instrumento:
        case "C2P":

            payload["datos"]["instrumento_c2p"] = instrumento

            if "instrumento_tdd" in payload["datos"].keys():

                del payload["datos"]["instrumento_tdd"]
        case "TDD":
            payload["datos"]["instrumento_tdd"] = instrumento

            if "instrumento_c2p" in payload["datos"].keys():

                del payload["datos"]["instrumento_c2p"]
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Tipo de instrumento no es C2P o TDD")


    logger.info(f"Payload: {json.dumps(payload)}")

    if MOCKUP:
        # Mockup es  true.
        now = datetime.now()
        datos = {
            "fecha_procesamiento": f"{now}",
            "estatus": "La solicitud de la clave temporal de pago se realizó de manera exitosa",
            "min_expiracion": "5"
        }
        return datos

    try:
        http_client = httpx.Client(verify=False)
        response = http_client.post(
            url_otp_mbu,
            headers=headers_pasarela_ms,
            json=payload,
            timeout=None
        )
    except httpx.RequestError as e:
        logger.error(f"Error en la solicitud: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )
    except httpx.ReadTimeout as e:
        logger.error(f"Tiempo de espera excedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Tiempo de espera excedido",
        )
    except httpx.HTTPError as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


    if response.status_code != 200:
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    resp = response.json()

    if resp["status"]["code"] != "EXITO":
        logger.error(f"{resp["status"]["description"]}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{resp["status"]["description"]}")


    return resp["datos"]





@router.post(
    "/consultar_tasa_bcv",
    response_model=ResponseTasaBCV,
    status_code=status.HTTP_200_OK,
    summary="Consulta Tasa BCV",
)
def consulta_tasa_bcv(
    request: TasaBCVBase,
    #client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
):
    data = request.model_dump()
    logger.info(f"Data: {data}")
    payload = payload_tasa_bcv.copy()

    payload["tasa"]["fe_tasa"] = data["fe_tasa"]

    logger.info(f"Header:{headers_suscripcion_ms}")
    logger.info(f"URL: {url_suscripcion_tasa_bcv}")
    logger.info(f"Payload: {payload}")

    try:
        http_client = httpx.Client(verify=False)
        response = http_client.post(
            url_suscripcion_tasa_bcv,
            headers=headers_suscripcion_ms,
            json=payload,
            timeout=None
        )
    except httpx.RequestError as e:
        logger.error(f"Error en la solicitud: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )
    except httpx.ReadTimeout as e:
        logger.error(f"Tiempo de espera excedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Tiempo de espera excedido",
        )
    except httpx.HTTPError as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    if response.status_code != 200:
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    resp = response.json()

    if resp["status"]["code"] != "EXITO":
        logger.error(f"{resp["status"]["description"]}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{resp["status"]["description"]}")

    return resp["tasa"][0]



@router.post(
    "/notificacion",
    #response_model=ResponseOTPMBU,
    #status_code=status.HTTP_200_OK,
    summary="Registrar Notificacion Pago a MS",
)
def notificacion_pago(
    request: NotificacionPagoBase,
    #client: httpx.AsyncClient = Depends(get_client),
    #api_key: str = Security(api_key_verifier),
):
    data = request.model_dump()
    tipo_pago = data.get("tipo_pago").value

    payload = payload_notificacion_pago.copy()
    payload["datos"]["poliza_recibo_cuota"] = data["poliza_recibo_cuota"]
    payload["datos"]["tipo_instrumento_pago"] = data["tipo_instrumento_pago"]
    payload["datos"]["nombre_pagador"] = data["nombre_pagador"]

    match tipo_pago:
        case "USD":
            payload["datos"]["notificar_estandar"] = {
                "moneda_pago": data["notificacion_pago"]["moneda_pago"].value,
                "monto_pago": data["notificacion_pago"]["monto_pago"],
                "cd_aprobacion": data["notificacion_pago"]["cd_aprobacion"]
            }
            try:
                del(payload["datos"]["notificar_multimoneda"])
            except KeyError:
                ...
        case "BS":
            payload["datos"]["notificar_multimoneda"] = {
                "moneda_pago": data["notificacion_pago"]["moneda_pago"].value,
                "monto_pago": data["notificacion_pago"]["monto_pago"],
                "cd_aprobacion": data["notificacion_pago"]["cd_aprobacion"],
                "moneda_recibo": data["notificacion_pago"]["moneda_recibo"],
                "monto_recibo": data["notificacion_pago"]["monto_recibo"],
                "tasa_cambio": data["notificacion_pago"]["tasa_cambio"]
            }
            try:
                del(payload["datos"]["notificar_estandar"])
            except KeyError:
                ...
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Tipo de pago tiene que ser USD o BS")

    try:
        logger.info(json.dumps(payload))
        logger.info(f"URL:{url_notificacion_pago}")
        logger.info(f"HEADER: {headers_pasarela_ms}")
        http_client = httpx.Client(verify=False)
        response = http_client.post(
            url_notificacion_pago,
            headers=headers_pasarela_ms,
            json=payload,
            timeout=None
        )
    except httpx.RequestError as e:
        logger.error(f"Error en la solicitud: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor",
        )
    except httpx.ReadTimeout as e:
        logger.error(f"Tiempo de espera excedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Tiempo de espera excedido",
        )
    except httpx.HTTPError as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    if response.status_code != 200:

        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":

        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")


    # # Convierte la respuesta en JSON
    response_json = response.json()
    result = response_json.get("datos")
    return result
