from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Dict, Union
from enum import Enum


class TipoDocumento(Enum):
    VEN = 'VEN'
    PVEN = 'PVEN'
    OPPA = 'OPPA'
    POCD = 'POCD'

class Sexo(Enum):
    M = 'M'
    F = 'F'


class PersonaTelefono(BaseModel):
    nu_consecutivo_telefono: int
    st_telefono: int
    cd_canal_informacion: int
    cd_pais: int
    tp_telefono: int
    nu_area: int
    nu_telefono: int

class PersonaDireccion(BaseModel):
    tp_via: int
    nm_calle: str
    cd_pais: int
    cd_provincia: int
    cd_zona: int
    di_fiscal: int
    tp_direccion: int
    cd_codigo_postal: str
    nu_piso: str
    di_completa: str
    nu_consecutivo_direccion: int
    di_postal: int
    st_direccion: int
    nu_puerta: str
    nu_casa: str
    cd_municipio: int
    nu_escalera: str
    cd_ciudad: int
    tp_vivienda: int
    de_observacion: str
    di_cobro: int


class PersonaEmail(BaseModel):
    cd_canal_informacion: int
    st_email: int
    de_email: str
    tp_email: int
    nu_consecutivo_email: int


class PersonaResponseBase(BaseModel):
    fe_inactivo: str
    cd_persona_representante_legal: str
    de_actividades_ilicitas: str
    in_rol_benef_preferencial: str
    cd_actividad_deportiva: str
    nm_segundo_apellido: str
    in_bloquear_cobro: str
    nu_documento_seccion4: str
    nu_documento_seccion3: str
    cd_provincia_nacimiento: int
    cd_segmentacion_persona: str
    va_resultado_riesgo: str
    nu_proximo_consec_tp_documento: int
    nm_cheque: str
    fe_ultima_verificacion: str
    cd_persona_asesor_juridico: str
    tp_empresa: str
    cd_ingreso_anual_dolar_princip: int
    tp_tax_identification: str
    fe_fallecimiento: str
    persona_telefono: List[PersonaTelefono]
    cd_oficio_riesgo: int
    cd_empresa: str
    nm_siglas_comercial: str
    cd_empleado: str
    cd_pais_nacimiento: str
    cd_estado_civil: str
    nu_tax_identification: str
    tp_canal_informacion: str
    in_accionista_superior_a: str
    in_candidato_componente_excl: str
    in_incapacitado: str
    in_vip: str
    nu_documento: str
    in_pep: str
    cd_sucursal_envio: int
    nm_primer_apellido: str
    in_bloqueo_pago: str
    fe_primera_verificacion: str
    in_inactivo: str
    nm_apellido_casada: str
    in_residente_pais: str
    in_sujeto_obligado: str
    cd_ingreso_anual: int
    de_observacion_inactivo: str
    fe_nacimiento: str
    persona_direccion: List[PersonaDireccion]
    cd_causa_inactivo: str
    persona_email: List[PersonaEmail]
    cd_persona: int
    cd_entidad_envio: int
    de_justifica_renglon_prima: str
    de_ingreso_adicional: str
    cd_pais_residencia: int
    cd_usuario: str
    nm_primer_nombre: str
    cd_ciudad_nacimiento: int
    cd_envio: int
    de_observacion: str
    in_persona_especial_fiscal: str
    cd_actividad: int
    cd_profesion: int
    cd_afinidad: str
    cd_dependencia3: str
    di_verificador: str
    cd_dependencia2: str
    cd_persona_agente_residente: str
    cd_dependencia1: str
    in_residente_accionista_eeuu: str
    nu_ideaseg: int
    nm_segundo_nombre: str
    de_aviso_operaciones: str
    tp_documento: str
    nu_registro: str
    tp_persona: int
    nu_ultimo_acuerdo_pago: str
    de_empresa: str
    tp_riesgo_persona: int
    in_lista_negra: str
    nu_rif: str
    cd_grupo_persona: str
    nu_endoso_formulario_cliente: str
    in_pago_exterior: str
    nu_tomo: str
    cd_sector: str
    nm_zonarazonsocial: str
    nu_documento_seccion2: str
    nu_documento_seccion1: str
    cd_ocupacion: int
    fe_vcto_registro_mercantil: str
    fe_ingreso_sistema: str
    in_actividades_ilicitas: str
    fe_registro: str
    cd_renglon_prima: int
    cd_nacionalidad: str
    cd_sexo: str
    nu_proximo_endoso: int
    nm_razon_social: str
    fe_vencimiento_documento: str
    cd_ingreso_anual_dolar_otra: int
    de_act_economica_adicional: str


class CreadaPersonaResponse(BaseModel):
    nm_zonarazonsocial: str
    nu_documento: str
    tp_documento: str
    cd_persona: int


class CoberturaResponse(BaseModel):
    suma: int
    total_prima_bien: float
    prima: float
    de_garantia: str
    comision: int
    cd_garantia: int


class BienesResponse(BaseModel):
    nu_bien: int
    coberturas: List[CoberturaResponse]


class CotizacionResponse(BaseModel):
    de_plan_pago: str
    mt_sig_cuota: float
    mt_suma: int
    nm_agente_bancario: str
    cd_plan_pago: int
    nu_item: int
    mt_prima_pago: float
    bienes: List[BienesResponse]
    de_plan: str
    in_seleccion: str
    mt_prima_total: float
    cd_moneda: int
    nu_total_cuota: int
    cd_entidad: int
    cd_plan: int
    nu_cotizacion: int
    cd_agente_bancario: str
    nu_sec_estructura: str


class MensajeResponse(BaseModel):
    id: int
    mensaje: str


class GarantiaResponse(BaseModel):
    mt_suma_aseg: int
    mt_comision: int
    de_garantia: str
    cd_garantia: int
    mt_prima: float


class CertificadoResponse(BaseModel):
    nu_convenio_pago: int
    nu_certificado: int
    nu_bien: int
    mt_prima_total: float
    cd_recibo: int
    garantias: List[GarantiaResponse]
    nu_orden_pago: str
    nu_endoso: int
    de_bien: str


class EmisionResponse(BaseModel):
    de_plan: str
    nu_poliza: int
    nm_agente_bancario: str
    nu_secuencia_estructura: str
    cd_moneda: int
    mensajes: List[MensajeResponse]
    cd_entidad: int
    cd_plan: int
    cd_area: int
    cd_agente_bancario: str
    certificado: List[CertificadoResponse]


class CuotaConsultaPolizaResponse(BaseModel):
    nu_cuota: int
    fe_st_cuota: str
    mt_pendiente: float
    cd_status_cuota: int
    mt_pendiente_sin_igtf: float
    mt_cuota: float
    de_status_cuota: str
    fe_vencimiento_cuota: str
    tp_cuota: str
    mt_pagado: int


class MediadorConsultaPolizaResponse(BaseModel):
    cd_mediador_especial: str
    nm_mediador_especial: str
    cd_mediador: int
    cd_persona_mediador_especial: str
    po_participacion_mediador: int
    cd_persona_mediador: int
    nm_mediador: str
    in_mediador_principal: int


class ReciboConsultaPolizaResponse(BaseModel):
    nu_convenio_pago: int
    fe_emision_recibo: str
    de_status_recibo: str
    fe_desde_recibo: str
    cd_recibo: int
    fe_hasta_recibo: str
    tp_transaccion: int
    mt_prima: float
    mt_igtf: float
    cuotas: List[CuotaConsultaPolizaResponse]
    mt_recibo: float
    cd_status_recibo: int


class CertificadoConsultaPolizaResponse(BaseModel):
    cd_persona_asegurada: int
    des_producto: str
    fe_proxima_facturacion: str
    de_plan_pago: str
    fe_desde_cert: str
    nu_certificado: int
    cd_plan_pago: int
    nu_ultimo_convenio_pago: str
    de_status_cert: str
    recibos: List[ReciboConsultaPolizaResponse]
    fe_hasta_cert: str
    nu_ultimo_endoso: int
    cd_status_cert: int
    cd_producto: int
    fe_emision_certificado: str
    mediadores: List[MediadorConsultaPolizaResponse]
    fe_ultimo_endoso: str


class PolizaConsultaResponse(BaseModel):
    cd_persona_contratante: int
    cd_sucursal: int
    tp_contrato: str
    nm_agente_bancario: str
    de_moneda: str
    tp_negocio: str
    certificados: List[CertificadoConsultaPolizaResponse]
    tp_facturacion: str
    afinidad: str
    nu_poliza: int
    nu_secuencia_estructura: str
    cd_moneda: int
    fe_emision_poliza: str
    cd_entidad: int
    cd_area: int
    cd_agente_bancario: str


class PolizasConsultaResponse(BaseModel):
    polizas: List[PolizaConsultaResponse]


class AnexoResponse(BaseModel):
    cd_persona_asegurada: str
    nm_anexo: str
    nu_consecutivo_anexo: str
    nu_certificado: str
    fe_exclusion: str
    tp_inclusion_anexo: str
    cd_producto: str
    fe_inclusion: str
    in_manual: str
    de_st_certificado: str
    cd_area_anexo: str
    de_tp_inclusion_anexo: str
    nm_zonarazonsocial: str
    nu_poliza: str
    de_entidad: str
    de_cd_area: str
    cd_entidad: str
    cd_anexo: str
    cd_area: str
    de_producto: str
    st_certificado: str
    nu_endoso: str


class AnexosConsultaResponse(BaseModel):
    anexo: List[AnexoResponse]

