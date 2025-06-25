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
from app.utils.v1.constants import (
    url_registrar_pago,
    headers_pasarela_ms,
    url_otp_mbu,
    headers_suscripcion_ms,
    url_suscripcion_tasa_bcv,
    url_notificacion_pago,
    headers_notificacion_pago_ms,
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
    api_key: str = Security(api_key_verifier),
):
    """
    Handles the registration of a payment via a payment gateway. This function extracts necessary
    payment information from a request, processes the data, constructs a payload, and sends it to
    the payment gateway. It supports multiple types of payment instruments, such as C2P, TDD,
    and TDC, and ensures correct processing of each type. In case of errors during the operation,
    appropriate HTTP exceptions are raised.

    Args:
        request (RegistroPagoBase): Request payload containing payment details and policy receipt.
        client (httpx.AsyncClient, optional): Asynchronous HTTP client used for making requests.
        api_key (str): Security token for verifying the request.

    Returns:
        dict: Parsed data from the payment gateway response.

    Raises:
        HTTPException: Raised with a 400 status if the payment instrument type is invalid, with a
            408 status if the request times out, with a 500 status for internal server errors,
            and with other statuses and messages specific to the payment gateway response.
    """
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
            # instrumento["numero"] = instrumento_c2p.get("numero")
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
        logger.error(f"{response.text}")
        detail = f"{response.text}"
        raise HTTPException(status_code=response.status_code,
                            detail=detail)

    if response.json()["status"]["code"] != "EXITO":

        logger.error(f"{response.text}")
        detail = f"{response.text}"
        raise HTTPException(status_code=response.status_code,
                            detail=detail)


    # # Convierte la respuesta en JSON
    response_json = response.json()
    result = response_json.get("datos")
    logger.info(json.dumps(result))
    return result




@router.post(
    "/otp_mbu",
    # response_model=ResponseOTPMBU,
    status_code=status.HTTP_200_OK,
    summary="Generar OTP Banco Mercantil",
)
def otp_mbu(
    request: OtpMbuBase,
    #client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
):
    """
    Handles the OTP generation and submission process for specified payment modalities. This
    function routes POST requests to the `/otp_mbu` endpoint, performs input validation, constructs
    the required payload for OTP processing, sends the payload to the backend service, and evaluates
    the response. It supports two types of instruments: `C2P` and `TDD`.

    Args:
        request (OtpMbuBase): Encapsulates the request data containing the required information
            to process the OTP for the specific instrument. The request must conform to the
            structure defined by `OtpMbuBase`.
        api_key (str): The API key required for securing the operation and authenticating the
            incoming request.

    Raises:
        HTTPException: Raised for any of the following cases:
            - If `tipo_instrumento` is neither `C2P` nor `TDD`.
            - For unsuccessful HTTP responses with a status code other than 200.
            - If the server encounters internal errors, timeout, or other critical issues.
            - For failed OTP processing responses where the backend does not return success status.

    Returns:
        dict: Contains the processed response details, including expiration details or statuses,
            depending on the backend service output. For mock operations, it includes simulated
            metadata like processing time and expiration information.
    """
    data = request.model_dump()
    logger.info(f"Data: {data}")
    tipo_instrumento = data.get("tipo_instrumento").value

    instrumento = data.get("instrumento")
    payload = payload_pasarela_otp.copy()
    payload["datos"]["tipo_instrumento_pago"] = tipo_instrumento

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
        logger.info(f"URL: {url_otp_mbu}")
        logger.info(f"Headers: {headers_pasarela_ms}")
        logger.info(f"Payload: {json.dumps(payload)}")
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
        logger.error(f"{response.text}")
        try:
            detail = f"{response.json()['status']['code']} {response.json()['status']['descripcion']}"
        except KeyError:
            detail = f"{response.text}"
        raise HTTPException(status_code=response.status_code,
                            detail=detail)

    resp = response.json()

    if resp["status"]["code"] != "EXITO":

        try:
            detail = f"{resp["status"]["description"]}"
        except KeyError:
            detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=detail)

    logger.info(f"Response: {resp}")
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
    """
    Handles the API endpoint for consulting the BCV exchange rate. This function receives
    a request object and an API key, processes the data, makes an HTTP request to a given
    endpoint, and returns the exchange rate information. The function logs all relevant
    steps, including payload details and error scenarios, while ensuring proper exception
    handling for request failures or server errors.

    Args:
        request (TasaBCVBase): The request object containing the data required for the
            BCV exchange rate query, such as the 'fe_tasa' field.
        api_key (str): A security credential provided for API access.

    Returns:
        dict: A dictionary object representing the queried BCV exchange rate, specifically
        the first exchange rate object from the 'tasa' list in the response.

    Raises:
        HTTPException: In cases where:
            - The server encounters an internal error during processing.
            - There is a timeout while waiting for the external service response.
            - There is an HTTP error during the HTTP request to the exchange rate service.
            - The response indicates an unsuccessful status (not equal to "EXITO").
            - The response status code is not 200.
    """
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
        logger.error(f"{response.text}")
        try:
            detail = f"{response.json()['status']['code']} {response.json()['status']['descripcion']}"
        except KeyError:
            detail = f"{response.text}"
        raise HTTPException(status_code=response.status_code,
                            detail=detail)

    resp = response.json()

    if resp["status"]["code"] != "EXITO":
        try:
            detail = f"{resp["status"]["description"]}"
        except KeyError:
            detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=detail)


    return resp["tasa"][0]



@router.post(
    "/notificacion",
    #response_model=ResponseOTPMBU,
    status_code=status.HTTP_200_OK,
    summary="Registrar Notificacion Pago a MS",
)
def notificacion_pago(
    request: NotificacionPagoBase,
    #client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
):
    """
    Handles the registration of a payment notification to the microservices system.

    This function processes the payment notification request, organizes its data into the
    appropriate payload format based on the type of payment, and sends the data to the
    configured endpoint. It also handles potential errors during the HTTP request and
    validates the response received from the server.

    Args:
        request (NotificacionPagoBase): An object containing the base data of the payment
            notification, including payment details and payer information.
        api_key (str): A security token used to validate the API request, provided by the
            Security dependency.

    Raises:
        HTTPException: If the payment type is not "USD" or "BS".
        HTTPException: If there is an error during the request to the microservices server,
            including server/internal errors, timeouts, or invalid response data.
        HTTPException: If the response does not indicate success (status code or details).

    Returns:
        Dict: A dictionary representing the success response data from the microservices,
        extracted from the "datos" key in the server's JSON response.
    """
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
        logger.info(f"HEADER: {headers_notificacion_pago_ms}")
        http_client = httpx.Client(verify=False)
        response = http_client.post(
            url_notificacion_pago,
            headers=headers_notificacion_pago_ms,
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

        logger.error(f"{response.text}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.text}")

    if response.json()["status"]["code"] != "EXITO":

        logger.error(f"{response.text}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.text} ")


    # # Convierte la respuesta en JSON
    response_json = response.json()
    result = response_json.get("datos")
    return result
