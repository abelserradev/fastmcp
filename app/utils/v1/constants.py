from app.utils.v1.configs import SM_ENDPOINT, SUBSCRIPTION_KEY, ENV

tipo_documento = {"V": "VEN", "E": "VEN", "P": "OPPA"}


frecuencia_cuota = {"MENSUAL": 201, "TRIMESTRAL": 202, "SEMESTRAL": 203, "ANUAL": 204}

url_consult_persona = f"{SM_ENDPOINT}/consultarpersona"
url_crear_persona = f"{SM_ENDPOINT}/crearpersona"
url_crear_poliza = f"{SM_ENDPOINT}/cotizaraccpersonales"
url_emitir_poliza = f"{SM_ENDPOINT}/emitirpoliza"
url_consultar_poliza = f"{SM_ENDPOINT}/consultarpoliza"
url_inclusion_anexos_poliza = f"{SM_ENDPOINT}/incanexpolivig"
url_cotizar = f"{SM_ENDPOINT}/cotizarglobal"
if ENV in ["production"]:
    url_cuadro_poliza = f"{SM_ENDPOINT}/swrep/executeRep"
else:
    url_cuadro_poliza = f"{SM_ENDPOINT}/swrep/ve/pru/executeRep"

headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
}

CORS_CONFIG = {
    "allow_origins":["*"],  # Allow all origins
    "allow_credentials":True,
    "allow_methods":["*"],  # Allow all methods
    "allow_headers":["*"]  # Allow all headers
}

PARENTESCO = {
    "CONYUGUE": 2,
    "HIJO": 3,
    "PADRE": 6,
    "MADRE": 7,
    "OTROS": 13
}

NU_TOTAL_CUOTAS = {
    "MENSUAL": 12,
    "TRIMESTRAL": 4,
    "SEMESTRAL": 2,
    "ANUAL": 1
}