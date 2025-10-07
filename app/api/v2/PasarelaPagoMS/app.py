import json


import httpx
from fastapi import APIRouter, HTTPException, Security, status
from app.middlewares.verify_api_key import APIKeyVerifier
from app.schemas.v2.PasarelaPagoMS.ModelAPI import RegistroPagoBase


from app.utils.v1.configs import API_KEY_AUTH, MID, MOCKUP
from app.utils.v1.constants import (
    url_registrar_pago,
    headers_pasarela_ms
)
from app.utils.v2.LoggerSingletonDB import logger
from app.utils.v1.messages_error import (
    INTERNAL_ERROR,
    TIMEOUT_ERROR,
    TIPO_INSTRUMENTO_ERROR,
)

from app.utils.v2.payload_templates import payload_pasarela_pago

router = APIRouter(
    tags=["Pasarela Pago MS Version 2"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)





@router.post(
    "/registrar_pago",
    status_code=status.HTTP_200_OK,
    summary="Registrar Pago Pasarela MS v2",
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

    # logger.info(f"Recibo poliza pago:{recibo_poliza_pago}")
    # logger.info(f"Moneda: {moneda_pago}")
    # logger.info(f"Tipo de instrumento de pago:{tipo_instrumento_pago}")
    # logger.info(f"Instrumento de pago: {instrumento}")
    payload_pasarela_pago["datos"]["poliza_recibo_cuota"] = recibo_poliza_pago
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=TIPO_INSTRUMENTO_ERROR)

    payload_pasarela_pago["datos"][tipo_instrumento] = instrumento



    try:
        # logger.info(f"URL:{url_registrar_pago}")
        # logger.info(f"HEADER: {headers_pasarela_ms}")
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
            detail=INTERNAL_ERROR,
        )
    except httpx.ReadTimeout as e:
        logger.error(f"Tiempo de espera excedido: {e}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=TIMEOUT_ERROR,
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



