import json
from typing import List

from fastapi import (
    APIRouter,
    Security,
    HTTPException,
    status
)
import requests

from app.api.Integration_SM.ModelAPI import ConsultarPersonaBase, CrearPersonaBase, CrearPolizaBase, EmitirPolizaBase, \
    ConsultarPolizaBase, InclusionAnexosPolizaBase, ConsultarRecibosPolizaBase, GetPolizasBase
from app.api.Integration_SM.ResponseModelAPI import (
    PersonaResponseBase,
    CreadaPersonaResponse,
    CotizacionResponse,
    CotizacionResponse,
    EmisionResponse,
    PolizasConsultaResponse,
    AnexosConsultaResponse
)
from app.middlewares.verify_api_key import APIKeyVerifier
from app.utils.LoggerSingleton import logger
from app.utils.configs import (
    API_KEY_AUTH,
    USER,
    APPLICATION, SUBSCRIPTION_KEY
)
from app.utils.constants import (
    tipo_documento,
    frecuencia_cuota,
    url_consult_persona,
    url_crear_persona,
    url_crear_poliza,
    url_emitir_poliza,
    headers,
    url_consultar_poliza,
    url_inclusion_anexos_poliza
)
from app.utils.payload_templates import (
    payload_persona,
    payload_cotizacion,
    payload_emitir_poliza, payload_consultar_poliza, payload_consultar_persona, payload_inclusion_anexos_poliza
)

router = APIRouter(
    tags=["SM"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


@router.post("/consultar_persona",  status_code=status.HTTP_200_OK, summary="Consultar persona en Seguros Mercantil")
def consultar_persona(request: ConsultarPersonaBase, api_key: str = Security(api_key_verifier)) -> dict:
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
    num_document = request.dict(exclude_unset=True)["num_documento"]

    # Determina el tipo de documento y ajusta el número de documento si es necesario
    tp_document = tipo_documento[num_document[0]]
    num_document = num_document[2:] if num_document[0] == "P" else num_document

    # Prepara el cuerpo de la solicitud para la API
    body = payload_consultar_persona.copy()
    body["persona"]["tp_documento"] = tp_document
    body["persona"]["nu_documento"] = num_document

    # Registra la solicitud en el log
    logger.info(f"body: {body}")
    logger.info(f"headers: {headers}")
    logger.info(f"url_consult_persona: {url_consult_persona}")

    # Realiza la solicitud a la API y registra la respuesta
    response =  requests.post(url_consult_persona, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # Convierte la respuesta en JSON
    response_json = json.loads(response.content)
    logger.info(f"Response: {response_json}")

    # Verifica el código de estado de la respuesta y retorna los datos correspondientes
    if response.status_code == 200:
        return response_json["persona"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_json)


@router.post("/crear_persona", response_model=CreadaPersonaResponse, status_code=status.HTTP_201_CREATED, summary="Crear persona en Seguros Mercantil")
def crear_persona(request: CrearPersonaBase, api_key: str = Security(api_key_verifier)) -> dict:
    """
        Crea una nueva persona en Seguros Mercantil.

        Este endpoint recibe los datos de una persona a través de un objeto `CrearPersonaBase` y los utiliza para crear una nueva persona
        en el sistema de Seguros Mercantil. La función prepara el cuerpo de la solicitud con los datos recibidos, ajustando el formato
        de la fecha de nacimiento y de registro a dd/mm/yyyy, y maneja la lógica para el tipo de documento, incluyendo el caso especial
        donde el número de documento comienza con 'P'. Finalmente, realiza una solicitud POST a la API de Seguros Mercantil y retorna
        el resultado de la operación.

        Args:
            request (CrearPersonaBase): Objeto Pydantic que contiene los datos de la persona a crear.
            api_key (str): Clave API proporcionada por el cliente para autenticación, verificada mediante `Security`.

        Returns:
            dict: Un diccionario que contiene el estado de la operación ('success' o 'error') y los datos de la persona creada
                  o el mensaje de error correspondiente.
    """
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
    logger.info(f"Response: {response_json}")
    # verificar si el request fue exitoso
    if response.status_code == 200:
        return response_json["persona"][0]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_json)


@router.post("/crear_cotizacion", response_model=CotizacionResponse,  status_code=status.HTTP_200_OK, summary="Crear cotizacion de persona en Seguros Mercantil")
def crear_cotizacion(request: CrearPolizaBase, api_key: str = Security(api_key_verifier)) -> dict:
    """
        Crea una póliza de seguro para una persona en Seguros Mercantil.

        Este endpoint recibe los datos necesarios para la creación de una póliza de seguro, incluyendo información personal
        del asegurado y detalles específicos de la póliza. Procesa esta información para construir el cuerpo de la solicitud
        adecuado para la API de Seguros Mercantil, realiza la solicitud y retorna el resultado.

        Args:
            request (CrearPolizaBase): Datos de la persona y la póliza a crear, validados por Pydantic.
            api_key (str): Clave API para autenticación, verificada mediante el middleware `Security`.

        Returns:
            dict: Un diccionario que indica el estado de la operación ('success' o 'error') y, dependiendo de este,
                  los datos de la póliza creada o el mensaje de error correspondiente.
    """

    data = request.dict(exclude_unset=True)
    logger.info(f"data: {data}")
    fecha_nacimiento = data["persona"]["fecha_nacimiento"].strftime("%d-%m-%Y")
    suma_poliza = data["poliza"]["suma_asegurada"] if "suma_asegurada" in data["poliza"].keys() else 250
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

    response = requests.post(url_crear_poliza, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)
    logger.info(f"Response: {response_json}")

    # verificar si el request fue exitoso
    if response.status_code == 200:
        return response_json["cotizacion"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_json)


@router.post("/emitir_poliza", response_model=EmisionResponse, status_code=status.HTTP_201_CREATED, summary="Emitir poliza de persona en Seguros Mercantil")
def emitir_poliza(request: EmitirPolizaBase, api_key: str = Security(api_key_verifier)) -> dict:
    """
        Emite una póliza de seguro para una persona en Seguros Mercantil.

        Este endpoint recibe los datos necesarios para la emisión de una póliza de seguro a través de un objeto `EmitirPolizaBase`.
        Procesa esta información para construir el cuerpo de la solicitud adecuado para la API de Seguros Mercantil. Realiza una
        solicitud POST a la API correspondiente y retorna el resultado de la operación.

        Args:
            request (EmitirPolizaBase): Datos necesarios para la emisión de la póliza, validados por Pydantic.

        Returns:
            dict: Un diccionario que indica el estado de la operación ('success' o 'error') y, dependiendo de este,
                  los datos de la póliza emitida o el mensaje de error correspondiente.
    """
    data = request.dict(exclude_unset=True)
    logger.info(f"data: {data}")
    logger.info(f"headers: {headers}")
    logger.info(f"url_emitir_poliza: {url_emitir_poliza}")
    body = payload_emitir_poliza.copy()
    body["coll_generales"]["generales"][0]["cd_entidad"] = data["cd_entidad"]
    body["coll_generales"]["generales"][0]["nu_cotizacion"] = data["nu_cotizacion"]
    logger.info(f"Body: {body}")

    response = requests.post(url_crear_poliza, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)
    logger.info(f"Response: {response_json}")
    # verificar si el request fue exitoso
    if response.status_code == 200:
        return response_json["emision"]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_json)

# response_model=PolizasConsultaResponse,
@router.post("/consultar_poliza", status_code=status.HTTP_200_OK, summary="Consultar poliza de persona en Seguros Mercantil")
def consultar_poliza(request: ConsultarPolizaBase, api_key: str = Security(api_key_verifier)) -> dict:
    """
        Consulta los detalles de una póliza específica en Seguros Mercantil.

        Este endpoint permite consultar los detalles de una póliza de seguro específica, utilizando varios criterios de búsqueda
        como la entidad, el área, el número de póliza, el certificado y el número de recibo. La información es enviada a la API
        de Seguros Mercantil, y se retorna la respuesta obtenida.

        Args:
            request (ConsultarPolizaBase): Objeto Pydantic que contiene los criterios de búsqueda para la consulta de la póliza.

        Returns:
            dict: Un diccionario que indica el estado de la operación ('success' o 'error') y, dependiendo de este,
                  los detalles de la póliza consultada o el mensaje de error correspondiente.
    """
    data = request.dict(exclude_unset=True)
    body = payload_consultar_poliza.copy()
    body["polizas-recibos"][0]["cd_entidad"] = data["cd_entidad"]
    body["polizas-recibos"][0]["cd_area"] = data["cd_area"]
    body["polizas-recibos"][0]["poliza"] = data["poliza"]
    body["polizas-recibos"][0]["certificado"] = data["certificado"]
    body["polizas-recibos"][0]["nu_recibo"] = data["nu_recibo"]

    response = requests.post(url_consultar_poliza, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)["polizas"]
    logger.info(f"Response: {response_json}")

    # verificar si el request fue exitoso
    if response.status_code == 200:
        return {"polizas":response_json}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_json)


@router.post("/incluir_anexo", response_model=AnexosConsultaResponse, status_code=status.HTTP_200_OK, summary="Incluir anexo poliza en Seguros Mercantil")
def incluir_anexo(request: InclusionAnexosPolizaBase, api_key: str = Security(api_key_verifier)) -> dict:
    data = request.dict(exclude_unset=True)
    name = f"{data['nm_primer_nombre']} {data['nm_primer_apellido']}"
    body = payload_inclusion_anexos_poliza.copy()
    body['cd_entidad'] = data['cd_entidad']
    body['cd_area'] = data['cd_area']
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

    response = requests.post(url_inclusion_anexos_poliza, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    #convertir response to JSON
    response_json = json.loads(response.content)
    logger.info(f"Response: {response_json}")

    #verificar si el request fue exitoso
    if response.status_code == 200:
       return {"anexo": response_json["anexo"]}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_json)


@router.post("/consultar_recibos", status_code=status.HTTP_200_OK, summary="Consultar recibos de una poliza de persona en Seguros Mercantil")
def consultar_recibos(request: ConsultarRecibosPolizaBase, api_key: str = Security(api_key_verifier)) -> dict:

    data = request.dict(exclude_unset=True)
    body = payload_consultar_poliza.copy()
    body["polizas-recibos"][0]["cd_entidad"] = data["cd_entidad"]
    body["polizas-recibos"][0]["cd_area"] = data["cd_area"]
    body["polizas-recibos"][0]["poliza"] = data["poliza"]
    body["polizas-recibos"][0]["certificado"] = data["certificado"]
    # del body["polizas-recibos"][0]["nu_recibo"]

    response = requests.post(url_consultar_poliza, data=json.dumps(body), headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    # convertir response to JSON
    response_json = json.loads(response.content)
    logger.info(f"Response: {response_json}")
    polizas = response_json.get("polizas", [])
    # verificar si el request fue exitoso
    if response.status_code == 200:
        return {"polizas":polizas}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_json)

