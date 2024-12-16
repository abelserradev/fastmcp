from app.utils.v1.configs import APPLICATION, USER


payload_cotizacion = {
    "coll_preguntas": {
        "preguntas": []
    },
    "persona": [],
    "funcionalidad": "COTIZAR_GLOBAL_IND_V",
    "aplicacion": APPLICATION,
    "usuario": USER,
    "coll_datos": {
        "datos": [
            {
                "cd_dato": "710055", # Cliente tarifa *configuracion*
                "nu_bien": "1",
                "valor": "19"
            },
            {
                "cd_dato": "710001", # País de residencia. 29 Venezuela
                "nu_bien": "1",
                "valor": "29"
            },
            {
                "cd_dato": "710038", # Plan Global Benefits *configuracion*
                "nu_bien": "1",
                "valor": "1"
            },
            {
                "cd_dato": "710034", # Deducible en Venezuela *fijo en 0*
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710035", # Deducible en el exterior *fijo en 0*
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710000", # Parentesco *fijo en 1 titular*
                "nu_bien": "1",
                "valor": "1"
            },
            {
                "cd_dato": "710037", # Fecha de nacimiento títular.
                "nu_bien": "1",
                "valor": "01/01/1980"
            },
            {
                "cd_dato": "710036", # Sexo títular
                "nu_bien": "1",
                "valor": "M"
            },
            {
                "cd_dato": "710003", # Número de hijos * Cero si no hay afiliados adicionales*
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710054", # Asistencia de viaje * Fijo en 0*
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710096", # Servicio funerario * valor fijo 0*
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710032", # Factpr de Ajuste comision *valor fijo 10 configuracion*
                "nu_bien": "1",
                "valor": "10"
            },
            {
                "cd_dato": "710200", # Dato interno sirweb valor fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710201", # Dato interno sirweb valor fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710202", # Dato interno sirweb valor fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710203",    # Dato interno sirweb valor fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710204", #Dato interno sirweb valor fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710205",    # Dato interno sirweb valor fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710206",  # Dato interno sirweb valor fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710207", # Dato interno sirweb fijo en 0
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710216", # Activación de cobertura de cuida salud fijo en 1
                "nu_bien": "1",
                "valor": "1"
            },
            {
                "cd_dato": "710089", # Deducible exterior de maternidad * valor fijo 0*
                "nu_bien": "1",
                "valor": "0"
            }
        ]
    },
    "coll_bienes": {
        "bienes": [
            {
                "in_seleccion": 1,
                "nu_bien": 1,
                "de_bien": "Jesus Prueba",  # Variable Nombre del asegurado.
            }
        ]
    },
    "coll_generales": {
        "generales": [
            {
                "nu_solicitud": "", #* Parámetro interno de sirweb valor fijo.
                "nu_cotizacion_mod": "", #* Parámetro interno de sirweb valor fijo.
                "cd_clase_riesgo": "S",  #*  Valor fijo S
                "cd_producto": "710100", #* Código de producto. valor fijo.
                "cd_persona_med": "11626", #*  Codigo persona asociado al agente. 11626.
                "di_ip": "0.0.0.0", #* dirección IP, fijado 0.0.0.0
                "in_web_externa": "", #* Parámetro interno de sirweb valor fijo ""
                "nu_poliza_relacionada": "", #* Parametro interno de sirweb valor fijo ""
                "in_solo_preparar": "0", #* INdicador procesamiento interno de sirweb valor fijo 0
                "cd_usuario": "INTERFAZSIRWEB", #* Codigo de usuario interno de sirweb, valor fijo INTERFAZSIRWEB
                "cd_moneda": "2", #* Codigo moneda, valor fijo 2.
                "cd_persona_med_agrupador": "", #* Parametro interno de sirweb valor fijo ""
                "cd_entidad": "1", #* Código de la entidad valor fijo 1.
                "de_observacion": "Plan Cuida Salud", #* Observacion ascoiada a la cotizacion generada en sirweb, valor fijo Plan Cuida Salud
                "ca_cuota": "1",  #* Cantidad de cuotas todos los casos es 1.
                "nu_sec_estructura": "", #* Parametro interno de sirweb valor fijo ""
                "cd_canal_venta": "39", #* Canal de venta valor 39.
                "cd_sucursal": "1", #* Sucursal asociada a la poliza, valor fijo 1.
                "nu_inspeccion": "", #* Parametro interno de sirweb valor fijo ""
                "cd_persona_med_especial": "", #* Parametro interno sirweb, valor fijo ""
                "nu_cot_relacionada": "", #* Parametro interno de sirweb, valor fijo ""
                "in_todos": "1", #* Parametro interno de sirweb valor fijo 1.
                "in_grabar": "1", #* Indicador procesamiento interno sirweb, valor fijo 1.
                "tp_mediador_especial": "", #*  Parametro interno de sirweb, valor fijo ""
                "nu_cotizacion_copia": "", #* Parametro interno de sirweb, valor fijo ""
                "cd_region": "1", #* Región asociada a la póliza, valor fijo 1.
                "cd_vigencia": "A", #* Código de la vigencia, valor fijo A.
                "cd_area": "71", #* Codigo de area del producto, valor fijo 71.
                "cd_plan_pago": "201", # <- Variable Código plan de pago
                "fe_desde": "03/10/2024", # <- variable fecha desde cobertura
                "fe_hasta": "03/10/2025", # <- variabble fecha hasta de cobertura
                "nu_documento_contratante": "V-19909340", # <- variable, documento contratante.
                "tp_documento_contratante": "VEN",  # <- variable, tipo documento contratante.
                "nu_documento": "V-19909340", # <- Número de documento: Para el títular. Si es menor de edad se maneja.
                "tp_documento": "VEN", # <- Tipo de documento.
                "cd_frecuencia_cuota": "M", # <- Variable Frecuencia de pago. Mensual: M, Trimestral: T, Semestral: S, Anual: A
                "nm_cliente": "CLIENTE PRUEBA", # <- variable: NOmbre del cliente títular.

            }
        ]
    },
    "coll_grpaseg": {"grpaseg": []},
}


payload_cuadro_poliza = {
    "funcionalidad": "OBTENER_CUADRO_POLIZA",
    "aplicacion": APPLICATION,
    "usuario": USER,
    "datos_poliza": {
        "cd_entidad": 0,
        "cd_area": 0,
        "nu_poliza": 0,
        "nu_certificado": 0,
        "nu_endoso": 0
    }
}

payload_consultar_cotizacion = {
    "aplicacion": APPLICATION,
    "funcionalidad": "CONSULTAR_COTIZACION_V",
    "usuario": USER,
    "cd_entidad": 0,
    "nu_cotizacion": 0,
    "cd_persona": "",
    "tp_documento": "",
    "nu_documento": "",
    "cd_persona_mediador": "",
    "cd_persona_mediador_especial": "",
    "cd_mediador": "",
    "cd_mediador_especial": "",
    "nu_secuencia_estructura": "",
    "cd_agente_bancario": "",
    "datos_cotizacion": [
        {
            "cd_dato": "",
            "va_dato": ""
        }
    ]
}