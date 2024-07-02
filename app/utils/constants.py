from app.utils.configs import APPLICATION, USER

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

tipo_documento = {
  "V": "VEN",
  "E": "VEN",
  "P": "PVEN"
}