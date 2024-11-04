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
from app.schemas.v2.Integracion_SM.ModelRequestBase import CrearPolizaBase,  SolicitudCuadroPolizaBase
from app.schemas.v2.Integracion_SM.ModelResponseBase import CotizacionResponse, CuadroPolizaResponse
from app.utils.v1.AsyncHttpx import fetch_url, get_client

from app.utils.v1.configs import API_KEY_AUTH, SUMA_ASEGURADA
from app.utils.v1.constants import (
    frecuencia_cuota,
    headers,
    tipo_documento,
    url_cotizar,
    NU_TOTAL_CUOTAS, url_cuadro_poliza
)
from app.utils.v1.LoggerSingleton import logger
from app.utils.v2.mockup_response_cotizacion import cotizacion

from app.utils.v2.payload_templates import payload_cotizacion, payload_cuadro_poliza

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
    data = request.model_dump(exclude_unset=True)
    logger.info(f"data: {data}")


    fecha_nacimiento = data["persona"]["fecha_nacimiento"]
    suma_poliza = SUMA_ASEGURADA
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
        # if item["cd_dato"] == 990150:
        #     item["valor"] = suma_poliza
        if item["cd_dato"] == "710037":
            item["valor"] = fecha_nacimiento
        if item["cd_dato"] == "710036":
            item["valor"] = sexo

        coll_datos["datos"].append(item)

    body["coll_datos"] = coll_datos
    logger.info(f"{json.dumps(body)}")


    # try:

    response = await fetch_url(
        "POST",
        url_cotizar,
        headers,
        body
    )
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = response.json()
    logger.info(f"Response: {response_json}")

    # verificar si el request fue exitoso
    if response.status_code == 200:
        return response_json["cotizacion"]
    else:
        logger.error(f"{response_json}")
        raise HTTPException(status_code=response.status_code,detail=f"{response_json['mensajes'][0]['mensaje']} {response_json['status']['descripcion']}" )

    # except httpx.RequestError as e:
    #     logger.error(f"Error en la solicitud: {e}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Error interno del servidor",
    #     )
    # except httpx.ReadTimeout as e:
    #     logger.error(f"Tiempo de espera excedido: {e}")
    #     raise HTTPException(
    #         status_code=status.HTTP_408_REQUEST_TIMEOUT,
    #         detail="Tiempo de espera excedido",
    #     )




@router.post(
    "/cuadro_poliza",
    #response_class=FileResponse,
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
    body = payload_cuadro_poliza.copy()
    logger.info(f"data: {data}")
    body["datos_poliza"] = data["datos_poliza"]
    logger.info(f"{json.dumps(body)}")

    try:
        response = await fetch_url(
            "POST",
            url_cuadro_poliza,
            headers,
            body
        )
        logger.info(f"Response status code: {response.status_code}")
        response_json = response.json()
        reporte_codificado = response_json["reporte_codificado"]

        # Decodificar base64 a PDF

        #pdf_stream = BytesIO(base64.b64decode(reporte_codificado))
        #pdf_stream = BytesIO(reporte_codificado)
        if response.status_code == 200 and response_json["status"]["code"] == "EXITO":
            return {
                "status": {
                    "code": "EXITO",
                    "descripcion": "EXITO"
                },
                "reporte_codificado": reporte_codificado
            }
            #return StreamingResponse(reporte_codificado, media_type="application/pdf")
        else:
            logger.error(f"{response_json}")
            raise HTTPException(status_code=response.status_code,detail=f"{response_json['mensajes'][0]['mensaje']} {response_json['status']['descripcion']}" )

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