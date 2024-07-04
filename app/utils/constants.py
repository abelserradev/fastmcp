from app.utils.configs import APPLICATION, USER, SM_ENDPOINT, SUBSCRIPTION_KEY

tipo_documento = {
  "V": "VEN",
  "E": "VEN",
  "P": "OPPA"
}


frecuencia_cuota = {
    "MENSUAL": 201,
    "TRIMESTRAL": 202,
    "SEMESTRAL": 203,
    "ANUAL": 204
}

url_consult_persona = f"{SM_ENDPOINT}/consultarpersona"
url_crear_persona = f"{SM_ENDPOINT}/crearpersona"
url_crear_poliza = f"{SM_ENDPOINT}/cotizaraccpersonales"
url_emitir_poliza = f"{SM_ENDPOINT}/emitirpoliza"
url_consultar_poliza = f"{SM_ENDPOINT}/consultarpoliza"

headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}