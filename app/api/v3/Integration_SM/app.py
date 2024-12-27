import json

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status



from app.middlewares.verify_api_key import APIKeyVerifier
from app.schemas.v3.Integracion_SM.ModelRequestBase import CrearPolizaBase
#from app.schemas.v3.Integracion_SM.ModelResponseBase import CotizacionResponse
#from app.utils.v1.AsyncHttpx import fetch_url, get_client

from app.utils.v1.configs import API_KEY_AUTH, SUMA_ASEGURADA
from app.utils.v1.constants import (
    frecuencia_cuota,
    headers,
    tipo_documento,
    url_cotizar
)
from app.utils.v1.LoggerSingleton import logger


# from app.utils.v3.payload_templates import payload_cotizacion

router = APIRouter(
    tags=["MS Integration Version 3"],
)

api_key_verifier = APIKeyVerifier(API_KEY_AUTH)


@router.post(
    "/crear_cotizacion_global",
    #response_model=CotizacionResponse,
    status_code=status.HTTP_200_OK,
    summary="Crear cotizacion de persona en Seguros Mercantil",
)
async def crear_cotizacion(
    request: CrearPolizaBase
):
    data = request.model_dump(exclude_unset=True)
#    payload = payload_cotizacion.copy()
#     datos = payload.get("coll_datos").get("datos").copy()
#
#
#     num_hijos = int(data.get("cantidad_hijos"))
#     tiene_conyugue = data.get("tiene_conyugue")
#     beneficiarios = data.get("beneficiarios", [])
#
#     if num_hijos > 0:
#         datos.append({
#             "cd_dato": "710003",  # Número de hijos.
#             "nu_bien": "1",
#             "valor": f"{num_hijos}"
#         })

    # if tiene_conyugue:
    #     fe_nac_conyugue = ""
    #     for beneficiario in beneficiarios:
    #         if beneficiario["cd_parentesco"] == "CONYUGUE"
    #             fe_nac_conyugue = beneficiario["fe_nacimiento"]
    #             break
    #
    #     datos.append(
    #         {
    #             "cd_dato": "710051",  # Fecha de nacimiento del conyuge. Se pasa si se tiene un conyugue vinculado.
    #             "nu_bien": "1",
    #             "valor": fe_nac_conyugue
    #         }
    #     )



    logger.info(f"data: {data}")
    return {"data": data}
