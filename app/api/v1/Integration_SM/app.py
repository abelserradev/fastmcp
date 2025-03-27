import json

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.schemas.v1.Integration_SM.ModelAPI import (ConsultarPersonaBase,
                                                    ConsultarPolizaBase,
                                                    ConsultarRecibosPolizaBase,
                                                    CrearPersonaBase,
                                                    CrearPolizaBase,
                                                    EmitirPolizaBase,
                                                    InclusionAnexosPolizaBase)
from app.schemas.v1.Integration_SM.ResponseModelAPI import (AnexosConsultaResponse,
                                                            CotizacionResponse,
                                                            CreadaPersonaResponse,
                                                            EmisionResponse)
from app.middlewares.verify_api_key import APIKeyVerifier
from app.utils.v1.AsyncHttpx import get_client, fetch_url
from app.utils.v1.configs import API_KEY_AUTH
from app.utils.v1.constants import (frecuencia_cuota, headers, tipo_documento,
                                    url_consult_persona, url_consultar_poliza,
                                    url_crear_persona, url_crear_cotizacion,
                                    url_emitir_poliza,
                                    url_inclusion_anexos_poliza)
from app.utils.v1.LoggerSingleton import logger
from app.utils.v1.payload_templates import (payload_consultar_persona,
                                            payload_consultar_poliza,
                                            payload_cotizacion,
                                            payload_emitir_poliza,
                                            payload_inclusion_anexos_poliza,
                                            payload_persona)
from app.utils.v2.SyncHttpx import sync_fetch_url

router = APIRouter(
    tags=["MS Integration Version 1"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


@router.post(
    "/consultar_persona",
    status_code=status.HTTP_200_OK,
    summary="Consultar persona en Seguros Mercantil",
)
async def consultar_persona(
    request: ConsultarPersonaBase,
    #client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Consulta la información de una persona en Seguros Mercantil utilizando su número de documento.

    Este endpoint recibe un objeto `ConsultarPersonaBase` que contiene el número de documento de la persona a consultar.
    El tipo de documento se determina por el primer carácter del número de documento. Si el primer carácter es 'P',
    se elimina para la consulta. La función construye el cuerpo de la solicitud para la API de consulta de persona,
    registra la solicitud en el log, realiza la solicitud a la API, registra la respuesta, y verifica el código de estado
    de la respuesta para retornar los datos correspondientes.

    Args:
        request (ConsultarPersonaBase): Objeto Pydantic que contiene el número de documento de la persona a consultar.
        api_key (str): Clave API proporcionada por el cliente para autenticación, verificada mediante `Security`.

    Returns:
        dict: Un diccionario que contiene el estado de la respuesta ('success' o 'error') y los datos de la persona consultada
              o el mensaje de error correspondiente.
    """

    # Extrae el número de documento de la solicitud y determina el tipo de documento
    num_document = request.model_dump(exclude_unset=True)["num_documento"]
    logger.info(f"data: {num_document}")
    # Determina el tipo de documento y ajusta el número de documento si es necesario
    tp_document = tipo_documento[num_document[0]]
    num_document = num_document[2:] if num_document[0] == "P" else num_document

    # Prepara el cuerpo de la solicitud para la API
    body = payload_consultar_persona.copy()
    body["persona"]["tp_documento"] = tp_document
    body["persona"]["nu_documento"] = num_document
    logger.info(f"Payload: {body}")



    try:
        response = await fetch_url(
            "POST",
            url_consult_persona,
            headers,
            body
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


    if response.status_code != 200:
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")


    # Convierte la respuesta en JSON
    response_json = response.json()
    logger.info(f"Response: {response_json}")
    persona = response_json.get("persona", [])


    return persona



@router.post(
    "/crear_persona",
    response_model=CreadaPersonaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear persona en Seguros Mercantil",
)
def crear_persona(
    request: CrearPersonaBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Args:
        request: The request payload containing the necessary information for creating a person.
        client: An asynchronous HTTP client dependency for making external API requests.
        api_key: Security dependency for verifying the API key.
    """
    try:
        data = request.model_dump(exclude_unset=True)
        logger.info(f"data: {data}")
        body = payload_persona.copy()
        nu_documento = (
            data["persona"]["documento"]["nu_documento"][2:]
            if data["persona"]["documento"]["nu_documento"][0] == "P"
            else data["persona"]["documento"]["nu_documento"]
        )
        tp_documento = tipo_documento[data["persona"]["documento"]["nu_documento"][0]]

        #fe_nacimiento = data["persona"]["fe_nacimiento"]
        #fe_registro = data["fe_registro"].strftime("%d/%m/%Y")
        body["persona"][0]["nm_primer_nombre"] = data["persona"]["nm_primer_nombre"]
        body["persona"][0]["nm_primer_apellido"] = data["persona"]["nm_primer_apellido"]
        body["persona"][0]["cd_sexo"] = data["persona"]["cd_sexo"].value
        body["persona"][0]["fe_nacimiento"] = data["persona"]["fe_nacimiento"]
        body["persona"][0]["fe_registro"] = data["fe_registro"]
        body["persona"][0]["persona_email"][0]["de_email"] = data["persona"]["contacto"][
            "de_email"
        ]
        body["persona"][0]["persona_telefono"][0]["nu_area"] = data["persona"]["contacto"][
            "nu_area_telefono"
        ]
        body["persona"][0]["persona_telefono"][0]["nu_telefono"] = data["persona"][
            "contacto"
        ]["nu_telefono"]
        body["persona"][0]["nu_documento"] = nu_documento
        body["persona"][0]["tp_documento"] = tp_documento
        body["persona"][0]["nu_documento_seccion2"] = nu_documento[2:]
        body["persona"][0]["nu_documento_seccion1"] = nu_documento[:1]
        body["persona"][0]["cd_nacionalidad"] = "VEN"
        body["persona"][0]["cd_pais_nacimiento"] = "VEN"
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )


    try:

        response = sync_fetch_url(
            "POST",
            url_crear_persona,
            headers,
            body
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

    if response.status_code != 200:
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")


    # convertir response to JSON
    response_json = response.json()
    logger.info(f"Response: {response_json}")
    # verificar si el request fue exitoso

    return response_json["persona"][0]



@router.post(
    "/crear_cotizacion",
    response_model=CotizacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Crear cotizacion de persona en Seguros Mercantil",
)
async def crear_cotizacion(
    request: CrearPolizaBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Args:
        request: The request object containing the input data for creating a policy quote.
        client: An asynchronous HTTP client used to make API calls.
        api_key: Security dependency for verifying the API key.

    """
    try:
        data = request.model_dump(exclude_unset=True)
        logger.info(f"data: {data}")
        fecha_nacimiento = data["persona"]["fecha_nacimiento"]
        suma_poliza = (
            data["poliza"]["suma_asegurada"]
            if "suma_asegurada" in data["poliza"].keys()
            else 250
        )
        fe_desde = data["poliza"]["fe_desde"].strftime("%d/%m/%Y")
        fe_hasta = data["poliza"]["fe_hasta"].strftime("%d/%m/%Y")
        cd_plan_pago = frecuencia_cuota[data["poliza"]["frecuencia_cuota"].value]
        nu_documento = (
            data["persona"]["documento"]["nu_documento"][2:]
            if data["persona"]["documento"]["nu_documento"][0] == "P"
            else data["persona"]["documento"]["nu_documento"]
        )
        tp_documento = tipo_documento[data["persona"]["documento"]["nu_documento"][0]]
        fullname = (
            f"{data['persona']['nm_primer_nombre']} {data['persona']['nm_primer_apellido']}"
        )

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

        coll_datos = {"datos": []}
        for item in body["coll_datos"]["datos"]:
            if item["cd_dato"] == 990150:
                item["valor"] = suma_poliza
            if item["cd_dato"] == 990160:
                item["valor"] = fecha_nacimiento
            coll_datos["datos"].append(item)

        body["coll_datos"] = coll_datos

    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    try:

        response = await fetch_url(
            "POST",
            url_crear_cotizacion,
            headers,
            body
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

    if response.status_code != 200:
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")





    # convertir response to JSON
    response_json = response.json()
    logger.info(f"Response: {response_json}")
    return response_json["cotizacion"]


@router.post(
    "/emitir_poliza",
    response_model=EmisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Emitir poliza de persona en Seguros Mercantil",
)
async def emitir_poliza(
    request: EmitirPolizaBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Args:
        request: Contiene los datos de la solicitud para emitir la póliza.
        client: Cliente HTTP asincrónico utilizado para hacer solicitudes.
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

        response = await fetch_url(
            "POST",
            url_emitir_poliza,
            headers,
            body
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

    if response.status_code != 200:
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")


    response_json = response.json()
    logger.info(f"Response: {response_json}")


    return response_json["emision"]



# response_model=PolizasConsultaResponse,
@router.post(
    "/consultar_poliza",
    status_code=status.HTTP_200_OK,
    summary="Consultar poliza de persona en Seguros Mercantil",
)
async def consultar_poliza(
    request: ConsultarPolizaBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Args:
        request: An instance of ConsultarPolizaBase, representing the body of the request to get the policy details.
        client: An asynchronous HTTP client dependency, provided by FastAPI's Depends function.
        api_key: A security dependency to verify the API key, provided by FastAPI's Security function.
    """
    try:
        data = request.model_dump(exclude_unset=True)
        logger.info(f"data: {data}")
        body = payload_consultar_poliza.copy()
        body["polizas-recibos"][0]["cd_entidad"] = data["cd_entidad"]
        body["polizas-recibos"][0]["cd_area"] = data["cd_area"]
        body["polizas-recibos"][0]["poliza"] = data["poliza"]
        body["polizas-recibos"][0]["certificado"] = data["certificado"]
        logger.info(f"antes: {body}")
        try:
            del body["polizas-recibos"][0]["nu_recibo"]
        except KeyError:
            ...

        if "nu_recibo" in data.keys():
            body["polizas-recibos"][0]["nu_recibo"] = data["nu_recibo"]
        logger.info(f"depues: {body}")

    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    try:
        logger.info(f"Payload:{body}")
        response = await fetch_url(
            "POST",
            url_consultar_poliza,
            headers,
            body
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
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")
    elif response.json()["status"]["code"] == "EXITO" and response.json()["status"]['descripcion'] == 'No se ha encontrado informacion para los criterios de busqueda indicados.':
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")


    response_json = response.json()
    logger.info(f"Response: {response_json}")
    return response_json



@router.post(
    "/incluir_anexo",
    response_model=AnexosConsultaResponse,
    status_code=status.HTTP_200_OK,
    summary="Incluir anexo poliza en Seguros Mercantil",
)
async def incluir_anexo(
    request: InclusionAnexosPolizaBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Args:
        request: Instance of InclusionAnexosPolizaBase containing the request data.
        client: An httpx.AsyncClient instance for making HTTP requests.
        api_key: A string representing the security API key.
    """
    try:
        data = request.model_dump(exclude_unset=True)
        logger.info(f"data: {data}")
        name = f"{data['nm_primer_nombre']} {data['nm_primer_apellido']}"
        body = payload_inclusion_anexos_poliza.copy()
        body["cd_entidad"] = data["cd_entidad"]
        body["cd_area"] = data["cd_area"]
        body["nu_poliza"] = data["nu_poliza"]
        # body["cd_anexo"]  = data["cd_anexo"]
        datos_dinamicos = body["datos_dinamicos"].copy()

        items = []
        for item in datos_dinamicos:
            if item["cd_dato"] == "&NU_POLIZA":
                item["va_dato"] = str(data["nu_poliza"])
            if item["cd_dato"] == "&NM_ASEGURADO":
                item["va_dato"] = name
            items.append(item)

        body["datos_dinamicos"] = items
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    try:

        response = await fetch_url(
            "POST",
            url_inclusion_anexos_poliza,
            headers,
            body
        )

        # convertir response to JSON

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
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")



    response_json = response.json()
    logger.info(f"Response: {response_json}")
    return {"anexo": response_json["anexo"]}




@router.post(
    "/consultar_recibos",
    status_code=status.HTTP_200_OK,
    summary="Consultar recibos de una poliza de persona en Seguros Mercantil",
)
async def consultar_recibos(
    request: ConsultarRecibosPolizaBase,
    client: httpx.AsyncClient = Depends(get_client),
    api_key: str = Security(api_key_verifier),
) -> dict:
    """
    Args:
        request: An instance of ConsultarRecibosPolizaBase containing the request data for retrieving policy receipts.
        client: An instance of httpx.AsyncClient which is used to make HTTP requests.
        api_key: A string representing the API key, verified through Security.

    Returns:
        dict: A dictionary containing the policy receipts data if the request is successful,
              otherwise raises an HTTPException with the appropriate status code and detail message.

    Raises:
        HTTPException: If the response status code is not 200 or if there is any request error or timeout.
    """
    try:
        data = request.model_dump(exclude_unset=True)
        logger.info(f"Data: {data}")
        body = payload_consultar_poliza.copy()
        body["polizas-recibos"][0]["cd_entidad"] = data["cd_entidad"]
        body["polizas-recibos"][0]["cd_area"] = data["cd_area"]
        body["polizas-recibos"][0]["poliza"] = data["poliza"]
        body["polizas-recibos"][0]["certificado"] = data["certificado"]


    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}",
        )

    try:

        response = await fetch_url(
            "POST",
            url_consultar_poliza,
            headers,
            body
        )

        # convertir response to JSON
        response_json = json.loads(response.content)
        logger.info(f"Response: {response_json}")
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
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")

    if response.json()["status"]["code"] != "EXITO":
        logger.error(f"{response.json()}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"{response.json()['status']['code']} {response.json()['status']['descripcion']}")



    polizas = response_json.get("polizas", [])
    return {"polizas": polizas}


