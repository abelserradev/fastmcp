from app.utils.configs import USER, APPLICATION

payload_persona = {
  "aplicacion": APPLICATION,
  "funcionalidad": "CREAR_PERSONA_V",
  "persona": [
    {
      "cd_estado_civil": "S",
      "nm_segundo_nombre": "",
      "nm_segundo_apellido": "",
      "cd_ocupacion": 999,
      "cd_oficio_riesgo": 1,
      "cd_pais_residencia": 29,
      "cd_profesion": 999,
      "persona_direccion": [
        {
          "nm_calle": "Noidentificada",
          "cd_pais": "29",
          "cd_provincia": "10",
          "cd_zona": "129",
          "cd_municipio": "1",
          "tp_direccion": "2",
          "cd_ciudad": "1",
          "tp_vivienda": "2"
        }
      ],
      "persona_rol": [
        {
          "cd_rol": 1
        }
      ],
      "persona_telefono": [
        {
          "cd_pais": "29",
          "tp_telefono": "7",
        }
      ],
      "persona_email": [
        {
          "tp_email": "13"
        }
      ],
      "persona_contacto": [],
      "persona_riesgo": [],
      "relacion_Personas_Juridicas": [],
      "pregunta_riesgo": [],
      "tp_persona": 1
    }
  ],
  "usuario": USER
}


payload_cotizacion = {
    "persona": [],
    "funcionalidad": "COTIZAR_ACCD_PERS_V",
    "aplicacion": APPLICATION,
    "usuario": USER,
    "coll_datos": {
        "datos": [
            {
                "cd_dato": 990150, # Suma asegurada
                "nu_bien": 1,
                "valor": 5000 # variable
            },
            {
                "cd_dato": 990140, # país residencia ven 29.
                "nu_bien": 1,
                "valor": "29"
            },
            {
                "cd_dato": 990141, # País de la tarifa ven 29
                "nu_bien": 1,
                "valor": "29"
            },
            {
                "cd_dato": 990160, # Fecha de nacimiento
                "nu_bien": 1,
                "valor": "01-01-1980" # Variable
            },
            {
                "cd_dato": 990205, # Goza de buena salud, fijo
                "nu_bien": 1,
                "valor": "S"
            },
            {
                "cd_dato": 100130, # Asistencia en viaje
                "nu_bien": 1,
                "valor": "0"
            },
            {
                "cd_dato": 100135, # Gastos médicos
                "nu_bien": 1,
                "valor": "1"
            }
        ]
    },
    "coll_bienes": {
        "bienes": [
            {
                "in_seleccion": 1,
                "in_grupo_asegurado": 1,
                "nu_bien": 1, # Variable fija.
                "in_asegurado": 1,
                "de_bien": "Jesus Prueba" # Variable
            }
        ]
    },
    "coll_generales": {
        "generales": [
            {
                "cd_clase_riesgo": "N",
                "fe_desde": "01/04/2022", # Variable
                "fe_hasta": "01/04/2023", # Variable
                "cd_producto": 100100,
                "cd_persona_med": 11626,
                "di_ip": "0.0.0.0",
                "in_solo_preparar": 0,
                "cd_usuario": "S3916",
                "cd_moneda": 2,
                "cd_entidad": "1",
                "cd_plan_pago": 204, # códigos mensual: 201, trimestral: 202, semestral: 203, anual:204
                "cd_frecuencia_cuota": "", # Dejar en blanco
                "ca_cuota": "", # Dejar en blanco
                "cd_canal_venta": 46,
                "cd_sucursal": "1",
                "nu_documento_contratante": "V-15500500", # Variable
                "tp_documento_contratante": "VEN", # Variable
                "nu_documento": "V-15500500", # Variable
                "tp_documento": "VEN", # Variable
                "in_todos": 0,
                "in_grabar": 1,
                "cd_region": 1,
                "nm_cliente": "Jesus Prueba", # Variable
                "cd_vigencia": "A",
                "cd_area": "1"
            }
        ]
    },
    "coll_grpaseg": {
        "grpaseg": []
    }
}


payload_emitir_poliza = {
    "aplicacion": APPLICATION,
    "funcionalidad": "EMITIR_POLIZA_V",
    "usuario": USER,
    "coll_generales": {
        "generales": [{
            "cd_entidad": 1, # variable
            "nu_cotizacion": 1168282, # variable
            "nu_item": 0, # Fijo
            "in_orden_pago": 0, # Fijo
            "in_emitir_futuro": 0 # Fijo
        }]
    }
}

payload_consultar_poliza = {
    "aplicacion": APPLICATION,
    "funcionalidad": "CONSULTAR_POL_REC_CUOTA_V",
    "usuario": USER,
    "polizas-recibos": [{
        "cd_entidad": 1,
        "cd_area": 71,
        "poliza": 145821,
        "certificado": 1,
        "nu_recibo": 1028810
    }]
}

payload_consultar_persona = {
        "aplicacion": APPLICATION,
        "funcionalidad": "CONSULTAR_PERSONA_V",
        "usuario": USER,
        "persona": {}
    }

payload_inclusion_anexos_poliza = {
    "aplicacion": APPLICATION,
    "funcionalidad": "INCLUIR_ANEXO_POL_VIG_V",
    "usuario": USER,
    "cd_entidad": 1, # Debe ser 1
    "cd_area": 1, # Debe ser 1
    "nu_poliza": 1640, # variable no de poliza
    "nu_certificado": 1, # Debe ser 1
    "cd_area_anexo": 1, # Debe ser 1
    "cd_anexo": 24, # variable.
    "in_texto_definido": 1, # Debe ser 1
    "tx_anexo_a_registrar": "", # debe ser ""
    "tp_inclusion_anexo": "F", # debe ser "F"
    "in_manual": 0, # debe ser 0
    "datos_dinamicos": [
        {
            "cd_dato": "&CD_ENTIDAD",
            "va_dato": "1" # debe ser "1"
        },
        {
            "cd_dato": "&CD_AREA",
            "va_dato": "1" # debe ser "1"
        },
        {
            "cd_dato": "&NU_POLIZA",
            "va_dato": "1640" # Variable no de poliza
        },
        {
            "cd_dato": "&NM_ASEGURADO",
            "va_dato": "Nombre Asegurado" # variable Nombre del asegurado.
        }
    ]
}