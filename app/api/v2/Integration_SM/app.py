import base64
import json
from ast import Bytes
from io import BytesIO

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status

from fastapi.responses import (
    StreamingResponse,
    FileResponse
)

from app.middlewares.verify_api_key import APIKeyVerifier
from app.schemas.v1.Integration_SM.ModelAPI import EmitirPolizaBase
from app.schemas.v1.Integration_SM.ResponseModelAPI import EmisionResponse
from app.schemas.v2.Integracion_SM.ModelRequestBase import CrearPolizaBase, SolicitudCuadroPolizaBase, \
    ConsultarCotizacionBase
from app.schemas.v2.Integracion_SM.ModelResponseBase import CotizacionResponse, CuadroPolizaResponse
from app.utils.v1.AsyncHttpx import fetch_url, get_client
from app.utils.v1.messages_error import INTERNAL_ERROR, TIMEOUT_ERROR
from app.utils.v2.SyncHttpx import get_sync_client, sync_fetch_url

from app.utils.v1.configs import API_KEY_AUTH, SUMA_ASEGURADA
from app.utils.v1.constants import (
    frecuencia_cuota,
    headers,
    tipo_documento,
    url_cotizar,
    NU_TOTAL_CUOTAS,
    url_cuadro_poliza,
    url_consultar_cotizacion, url_emitir_poliza
)
from app.utils.v2.LoggerSingletonDB import logger
from app.utils.v1.payload_templates import payload_emitir_poliza
from app.utils.v2.mockup_response_cotizacion import cotizacion

from app.utils.v2.payload_templates import payload_cotizacion, payload_cuadro_poliza, payload_consultar_cotizacion

router = APIRouter(
    tags=["MS Integration Version 2"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


@router.post(
    "/crear_cotizacion_global",
    response_model=CotizacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Crear cotizacion de persona en Seguros Mercantil",
)
async def crear_cotizacion(
    request: CrearPolizaBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
):
    """
    crear_cotizacion is an asynchronous function that creates a policy based on the provided request data.
    Args:
        request: Object containing the request data for policy creation.
        client: Async HTTP client dependency used to make network requests.
        api_key: API key for security verification.
    """
    try:
        data = request.model_dump(exclude_unset=True)
        logger.info(f"data: {data}")


        fecha_nacimiento = data["persona"]["fecha_nacimiento"]

        fe_desde = data["poliza"]["fe_desde"]
        fe_hasta = data["poliza"]["fe_hasta"]
        cd_plan_pago = frecuencia_cuota[data["poliza"]["frecuencia_cuota"].value]
        cd_frecuencia_cuota = data["poliza"]["frecuencia_cuota"].value[0]
        nu_documento = (
            data["persona"]["documento"]["nu_documento"][2:]
            if data["persona"]["documento"]["nu_documento"][0] == "P"
            else data["persona"]["documento"]["nu_documento"]
        )
        tp_documento = tipo_documento[data["persona"]["documento"]["nu_documento"][0]]
        fullname = (
            f"{data['persona']['nm_primer_nombre']} {data['persona']['nm_primer_apellido']}"
        )
        sexo = data['persona']['sexo'].value

        body = payload_cotizacion.copy()

        body["coll_bienes"]["bienes"][0]["de_bien"] = fullname

        body["coll_generales"]["generales"][0]["cd_plan_pago"] = f"{cd_plan_pago}"
        body["coll_generales"]["generales"][0]["fe_desde"] = fe_desde
        body["coll_generales"]["generales"][0]["fe_hasta"] = fe_hasta
        body["coll_generales"]["generales"][0]["nu_documento_contratante"] = nu_documento
        body["coll_generales"]["generales"][0]["tp_documento_contratante"] = tp_documento
        body["coll_generales"]["generales"][0]["nu_documento"] = nu_documento
        body["coll_generales"]["generales"][0]["tp_documento"] = tp_documento
        body["coll_generales"]["generales"][0]["cd_frecuencia_cuota"] = cd_frecuencia_cuota
        body["coll_generales"]["generales"][0]["nm_cliente"] = fullname

        coll_datos = {"datos": []}

        for item in body["coll_datos"]["datos"]:

            if item["cd_dato"] == "710037":
                item["valor"] = fecha_nacimiento
            if item["cd_dato"] == "710036":
                item["valor"] = sexo

            coll_datos["datos"].append(item)

        body["coll_datos"] = coll_datos
        logger.info(f"Payload: {body}")

    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    try:

        response = await fetch_url(
            "POST",
            url_cotizar,
            headers,
            body
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )

    # verificar si el request fue exitoso
    if response.status_code != 200:

        detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=response.status_code,
                            detail=detail)

    if response.json()["status"]["code"] != "EXITO":

        detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=response.status_code,
                            detail=detail)


    # convertir response to JSON
    response_json = response.json()
    logger.info(f"Response: {response_json}")
    return response_json["cotizacion"]





@router.post(
    "/cuadro_poliza",
    response_model=CuadroPolizaResponse,
    status_code=status.HTTP_200_OK,
    summary="Devuelve pdf con el cuadro de póliza",
)
async def get_cuadro_poliza(
    request: SolicitudCuadroPolizaBase,
    api_key: str = Security(api_key_verifier),
):
    """
    Args:
        request: An instance of `SolicitudCuadroPolizaBase` containing the input data needed to generate the policy frame PDF.
        api_key: A string used for API key verification via security dependency.
    """

    data = request.model_dump(exclude_unset=True)
    logger.info(f"data: {data}")
    body = payload_cuadro_poliza.copy()
    body["datos_poliza"] = data["datos_poliza"]
    logger.info(f"Payload:: {body}")


    try:
        response = await fetch_url(
            "POST",
            url_cuadro_poliza,
            headers,
            body
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )

    response_json = response.json()

    if response.status_code != 200:

        detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=response.status_code,
                            detail=detail)

    if response.json()["status"]["code"] != "EXITO":

        detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=response.status_code,
                            detail=detail)



    reporte_codificado = response_json["reporte_codificado"]
    response = {
        "status": {
            "code": "EXITO",
            "descripcion": "EXITO"
        },
        "reporte_codificado": reporte_codificado
    }
    logger.info(f"Response: {response['status']}")
    return response







@router.post(
    "/consultar_cotizacion",
    status_code=status.HTTP_200_OK,
    summary="Consultar cotizacion de persona en Seguros Mercantil",
)
async def consultar_cotizacion(request: ConsultarCotizacionBase, api_key: str = Security(api_key_verifier)):
    data = request.model_dump(exclude_unset=True)
    logger.info(f"Data: {data}")
    cd_entidad = data.get("cd_entidad")
    body = payload_consultar_cotizacion.copy()
    body["nu_cotizacion"] = data.get("nu_cotizacion")
    body["cd_entidad"] = cd_entidad
    logger.info(f"Payload: {body}")
    try:
        response = await fetch_url(
            "POST",
            url_consultar_cotizacion,
            headers,
            body
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )

    if response.status_code != 200:
        logger.error(f"{response.text}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {response.text}"
        )

    try:
        response_json = response.json()
        if response.status_code == 200 and len(response_json["mensajes"]) > 0:
            # try:
            #     detail = response_json["mensajes"][0]["mensaje"]
            # except KeyError:
            detail = f"{response.text}"
            logger.error(detail)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        cotizacion = response_json["cotizacion"][0]
        bienes = []
        for bien in response_json["cotizacion"][0]["bienes"]:
            temp = bien.copy()
            del (
                temp["fe_fallecimiento"],
                temp["datos"],
                temp["fe_exclusion"],
                temp["preguntas"],
                temp["nu_consec_tp_doc_asegurado"],
            )
            bienes.append(temp)

        response_data = {
            "de_plan_pago": cotizacion["de_plan_pago"],
            "fe_desde": cotizacion["fe_desde"],
            "fe_hasta": cotizacion["fe_hasta"],
            "cd_entidad": cotizacion["cd_entidad"],
            "nu_cotizacion": cotizacion["nu_cotizacion"],
            "nu_documento_contratante": cotizacion["nu_documento_contratante"],
            "tp_documento_contratante": cotizacion["tp_documento_contratante"],
            "nu_documento": cotizacion["nu_documento"],
            "tp_documento": cotizacion["tp_documento"],
            "nu_poliza": cotizacion["nu_poliza"],
            "mt_prima_total": cotizacion["mt_prima_total"],
            "cd_region": cotizacion["cd_region"],
            "nu_total_cuota": cotizacion["nu_total_cuota"],
            "cd_area": cotizacion["cd_area"],
            "nm_cliente": cotizacion["nm_cliente"],
            "de_st_cotizacion": cotizacion["de_st_cotizacion"],
            "bienes": bienes,
        }
        logger.info(f"Response: {response_data}")
        return response_data

    except json.JSONDecodeError as e:
        logger.error(f"Error: {response.text}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al decodificar la respuesta JSON: {e}: {response.text}",
        )





@router.post(
    "/emitir_poliza",
    status_code=status.HTTP_201_CREATED,
    summary="Emitir poliza de persona en Seguros Mercantil",
)
def emitir_poliza(
    request: EmitirPolizaBase,
    client: httpx.Client = Depends(get_sync_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Args:
        request: Contiene los datos de la solicitud para emitir la póliza.
        client: Cliente HTTP sincrónico utilizado para hacer solicitudes.
        api_key: Clave de API utilizada para la verificación de seguridad.
    """
    try:
        data = request.model_dump(exclude_unset=True)
        logger.info(f"data: {data}")
        body = payload_emitir_poliza.copy()
        body["coll_generales"]["generales"][0]["cd_entidad"] = data["cd_entidad"]
        body["coll_generales"]["generales"][0]["nu_cotizacion"] = data["nu_cotizacion"]

    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    try:

        response = sync_fetch_url(
            "POST",
            url_emitir_poliza,
            headers,
            body
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )

    logger.info(response.text)
    logger.info(response.status_code)

    if response.status_code != 200:

        detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=response.status_code,
                            detail=detail)

    if response.json()["status"]["code"] != "EXITO":

        detail = f"{response.text}"
        logger.error(detail)
        raise HTTPException(status_code=response.status_code,
                            detail=detail)


    response_json = response.json()
    logger.info(f"Response: {response_json}")


    return response_json["emision"]