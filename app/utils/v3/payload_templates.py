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
                "cd_dato": "710055",  # Valor Fijo
                "nu_bien": "1",
                "valor": "19"
            },
            {
                "cd_dato": "710001",  # Valor Fijo
                "nu_bien": "1",
                "valor": "29"
            },
            {
                "cd_dato": "710038",  # Valor Fijo
                "nu_bien": "1",
                "valor": "1"
            },
            {
                "cd_dato": "710034",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710035",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710054",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710096",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710032",  # Valor Fijo
                "nu_bien": "1",
                "valor": "10"
            },
            {
                "cd_dato": "710200",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710201",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710202",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710203",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710204",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710205",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710206",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710207",  # Valor Fijo
                "nu_bien": "1",
                "valor": "0"
            },
            {
                "cd_dato": "710216",  # Valor Fijo
                "nu_bien": "1",
                "valor": "1"
            },
            {
                "cd_dato": "710089",  # Valor Fijo
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
                "nu_solicitud": "",  # Valor fijo
                "nu_cotizacion_mod": "",  # Valor fijo
                "cd_clase_riesgo": "S",  # Valor fijo
                "cd_plan_pago": "201",
                # Variable  código de plan 201 Mensual, 202 Trimestral, 203 Semestral, 204 Anual.
                "fe_desde": "25/10/2024",  # , Variable Fecha desde póliza.
                "cd_producto": "710100",  # Valor fijo
                "cd_persona_med": "11626",  # Valor fijo
                "di_ip": "0.0.0.0",  # Valor fijo
                "in_web_externa": "",  # Valor fijo
                "nu_poliza_relacionada": "",  # Valor fijo
                "in_solo_preparar": "0",  # Valor fijo
                "fe_hasta": "25/10/2025",  # variable fecha hasta póliza.
                "cd_usuario": "INTERFAZSIRWEB",  # Valor fijo.
                "cd_moneda": "2",  # Valor fijo
                "cd_persona_med_agrupador": "",  # Valor fijo
                "cd_entidad": "1",  # Valor fijo.
                "de_observacion": "Plan Cuida Salud",  # Valor fijo
                "ca_cuota": "1",  # Variable cantidad de cuidas, frecuencia.
                "nu_sec_estructura": "",  # Valor fijo
                "cd_canal_venta": "39",  # Valor fijo
                "cd_sucursal": "1",  # Valor fijo
                "nu_inspeccion": "",  # Valor fijo
                "nu_documento_contratante": "V-19909380",  # Variable. Quien paga la póliza
                "cd_persona_med_especial": "",  # Valor fijo.
                "nu_documento": "V-19909380",  # Variable-Títuloar
                "cd_frecuencia_cuota": "M",  # Variable,cuota frecuencia.
                "nu_cot_relacionada": "",  # Valor fijo.
                "in_todos": "1",  # Valor fijo.
                "in_grabar": "1",  # Valor fijo.
                "tp_mediador_especial": "",  # Valor fijo
                "nu_cotizacion_copia": "",  # Valor fijo
                "cd_region": "1",  # Valor fijo.
                "nm_cliente": "PRUEBA CUIDASALUD",  # Variable, nombre titular.
                "cd_vigencia": "A",  # Valor fijo
                "tp_documento": "VEN",  # Variable, tipo documento titular.
                "cd_area": "71",  # Valor fijo.
                "tp_documento_contratante": "VEN"  # Variable, tipo documento contratante.
            }
        ]
    },
    "coll_grpaseg": {"grpaseg": []}
}


