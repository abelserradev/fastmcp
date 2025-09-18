import json

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status



from app.middlewares.verify_api_key import APIKeyVerifier
from app.schemas.v2.Integracion_SM.ModelResponseBase import CotizacionResponse

from app.schemas.v4.Integracion_SM.ModelRequestBase import CrearPolizaBase


from app.utils.v1.configs import API_KEY_AUTH, SUMA_ASEGURADA
from app.utils.v1.constants import (
    frecuencia_cuota,
    headers,
    tipo_documento,
    url_cotizar, PARENTESCO
)
from app.utils.v2.LoggerSingletonDB import logger
from app.utils.v2.SyncHttpx import sync_fetch_url

from app.utils.v3.payload_templates import payload_cotizacion

router = APIRouter(
    tags=["MS Integration Version 4"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


@router.post(
    "/crear_cotizacion_global",
    response_model=CotizacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Crear cotizacion de persona en Seguros Mercantil",
)
def crear_cotizacion(
        request: CrearPolizaBase,
        #client: httpx.AsyncClient = Depends(get_client),
        api_key: str = Security(api_key_verifier),
):
    data = request.model_dump(exclude_unset=True)

    # logger.info(f"data: {data}")
    payload = payload_cotizacion.copy()
    # logger.info(f"Payload:{payload}")

    datos = payload.get("coll_datos").get("datos").copy()
    generales = payload.get("coll_generales").get("generales")


    num_hijos = int(data.get("cantidad_hijos",0))
    tiene_conyuge = data.get("tiene_conyuge", False)
    tiene_padre = data.get("tiene_padre", False)
    tiene_madre = data.get("tiene_madre", False)
    beneficiarios = data.get("beneficiarios", [])

    if num_hijos > 0:
        datos.append({
            "cd_dato": "710003",  # Número de hijos.
            "nu_bien": "1",
            "valor": f"{num_hijos}"
        })
    #
    if tiene_conyuge:
        fe_nac_conyuge = ""
        for beneficiario in beneficiarios:
            parentesco = beneficiario.get("cd_parentesco").value
            if parentesco == "CONYUGE":
                fe_nac_conyuge = beneficiario["fe_nacimiento"]
                break

        datos.append(
            {
                "cd_dato": "710051",  # Fecha de nacimiento del conyuge. Se pasa si se tiene un conyuge vinculado.
                "nu_bien": "1",
                "valor": fe_nac_conyuge
            }
        )

    if tiene_padre:
        fe_nac_padre = ""
        for beneficiario in beneficiarios:
            parentesco = beneficiario.get("cd_parentesco").value
            if parentesco == "PADRE":
                fe_nac_padre = beneficiario["fe_nacimiento"]
                break

        datos.append(
            {
                "cd_dato": "710057",  # Fecha de nacimiento del padre.
                "nu_bien": "1",
                "valor": fe_nac_padre
            }
        )

    if tiene_madre:
        fe_nac_madre = ""
        for beneficiario in beneficiarios:
            parentesco = beneficiario.get("cd_parentesco").value
            if parentesco == "MADRE":
                fe_nac_madre = beneficiario["fe_nacimiento"]
                break

        datos.append(
            {
                "cd_dato": "710060",  # Fecha de nacimiento del conyuge. Se pasa si se tiene un conyuge vinculado.
                "nu_bien": "1",
                "valor": fe_nac_madre
            }
        )

    nombre_titular = f"{data['titular']['nm_primer_nombre']} {data['titular']['nm_primer_apellido']}"


    nu_documento_titular = (
        data["titular"]["documento"]["nu_documento"][2:]
        if data["titular"]["documento"]["nu_documento"][0] == "P"
        else data["titular"]["documento"]["nu_documento"]
    )
    tp_documento_titular = tipo_documento[data["titular"]["documento"]["nu_documento"][0]]

    sexo_titular = data['titular']['sexo'].value
    fecha_nacimiento_titular = data['titular']['fecha_nacimiento']

    logger.info(nombre_titular)
    logger.info(f"documento: {nu_documento_titular}")
    logger.info(tp_documento_titular)
    logger.info(sexo_titular)
    logger.info(fecha_nacimiento_titular)

    nombre_contratante = f"{data['contratante']['nm_primer_nombre']} {data['contratante']['nm_primer_apellido']}"

    nu_documento_contratante = (
        data["contratante"]["documento"]["nu_documento"][2:]
        if data["contratante"]["documento"]["nu_documento"][0] == "P"
        else data["contratante"]["documento"]["nu_documento"]
    )
    tp_documento_contratante = tipo_documento[data["contratante"]["documento"]["nu_documento"][0]]

    sexo_contratante = data['contratante']['sexo'].value
    fecha_nacimiento_contratante = data['contratante']['fecha_nacimiento']



    fe_desde = data['poliza']['fe_desde']
    fe_hasta = data['poliza']['fe_hasta']
    frecuencia = data['poliza']['frecuencia_cuota']

    datos.extend(
        [
            {
                "cd_dato": "710000",
                "nu_bien": "1",
                "valor": "1"
            },
            {
                "cd_dato": "710037",  # Fecha nacimiento títular. dd/mm/yyy
                "nu_bien": "1",
                "valor": fecha_nacimiento_titular
            },
            {
                "cd_dato": "710036",  # Sexo del títular F/M.
                "nu_bien": "1",
                "valor": sexo_titular
            }
        ]
    )
    logger.info(f"Datos: {json.dumps(datos)}")
    bien = {
        "in_seleccion": "1",
        "nu_bien": "1",
        "de_bien": nombre_titular
    }
    general = generales[0]
    cd_plan_pago = frecuencia_cuota[frecuencia.value]
    general["cd_plan_pago"] = cd_plan_pago
    general["fe_desde"] = fe_desde
    general["fe_hasta"] = fe_hasta
    general["ca_cuota"] = "1"
    general["nu_documento_contratante"] = nu_documento_contratante
    general["nu_documento"] = nu_documento_titular
    general["cd_frecuencia_cuota"] = frecuencia.value[0]
    general["nm_cliente"] = nombre_titular
    general["tp_documento"] = tp_documento_titular
    general["tp_documento_contratante"] = tp_documento_contratante
    grpasegs = []

    for index,beneficiario in enumerate(beneficiarios):

        grpasegs.append(
            {
                "cd_parentesco": PARENTESCO[beneficiario["cd_parentesco"].value],
                "nu_consecutivo_asegurado": f"{index+1}",
                "nu_bien": "1",
                "nu_documento": (beneficiario["nu_documento"][2:] if beneficiario["nu_documento"][0] == "P" else beneficiario["nu_documento"]),
                "fe_nacimiento": beneficiario["fe_nacimiento"],
                "nm_primer_nombre": beneficiario["nm_primer_nombre"],
                "cd_sexo": beneficiario["cd_sexo"].value,
                "tp_documento": tipo_documento[beneficiario["nu_documento"][0]],
                "in_accion": "I",
                "nm_primer_apellido": beneficiario["nm_primer_apellido"]
            }
        )


    # Removed key in a dictionary
    payload.pop("coll_bienes")
    payload.pop("coll_datos")
    payload.pop("coll_generales")
    payload.pop("coll_grpaseg")
    logger.info(f"Payload to requests: {payload}")
    payload["coll_datos"] = {"datos": datos}
    payload["coll_bienes"] = {"bienes": [bien]}
    payload["coll_generales"] = {"generales": [general]}
    payload["coll_grpaseg"] = {"grpaseg": grpasegs}
    try:
        logger.info(f"URL-> {url_cotizar}")
        logger.info(f"Payload-> {json.dumps(payload)}")
        logger.info(f"headers-> {headers}")
        response = sync_fetch_url(
            "POST",
            url_cotizar,
            headers,
            payload
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
