import json
from typing import Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.middlewares.verify_api_key import APIKeyVerifier
from app.schemas.v1.PasarelaPagoMS.ModelAPI import RegistroPagoBase
from app.schemas.v1.PasarelaPagoMS.ResponseModelAPI import ResponsePagoBase
from app.utils.v1.AsyncHttpx import get_client, fetch_url
from app.utils.v1.configs import API_KEY_AUTH, MID
from app.utils.v1.constants import (url_registrar_pago,
                                    headers_pasarela_ms
                                    )
from app.utils.v1.LoggerSingleton import logger
from app.utils.v2.payload_templates import payload_pasarela_pago

router = APIRouter(
    tags=["Pasarela Pago MS Version 1"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


@router.post(
    "/registrar_pago",
    response_model=ResponsePagoBase,
    status_code=status.HTTP_200_OK,
    summary="Registrar Pago Pasarela MS",
)
async def registrar_pago(
    request: RegistroPagoBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> Dict:

    data = request.model_dump()

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
    payload_pasarela_pago["datos"]["tipo_instrumento"] = tipo_instrumento_pago
    payload_pasarela_pago["datos"]["moneda_pago"] = moneda_pago
    match tipo_instrumento_pago:
        case "TDD":
            tipo_instrumento = "instrumento_tdd"
        case "C2P":
            tipo_instrumento = "instrumento_c2p"
        case "TDC":
            tipo_instrumento = "instrumento_tdc"
        case _:
            ...

    payload_pasarela_pago["datos"][tipo_instrumento] = instrumento


    try:
        response = await fetch_url(
            "POST",
            url_registrar_pago,
            headers_pasarela_ms,
            payload_pasarela_pago
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )
    finally:
        try:
            del (payload_pasarela_pago["datos"][tipo_instrumento])
        except:
            ...


    if response.status_code != 200:
        try:
            del (payload_pasarela_pago["datos"][tipo_instrumento])
        except:
            ...

        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        try:
            del (payload_pasarela_pago["datos"][tipo_instrumento])
        except:
            ...

        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")



    # # Convierte la respuesta en JSON
    response_json = response.json()
    datos = response_json.get("datos")
    return datos


