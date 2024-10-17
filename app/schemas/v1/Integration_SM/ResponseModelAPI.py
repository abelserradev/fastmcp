
from enum import Enum
from typing import List

from pydantic import BaseModel


class TipoDocumento(Enum):
    """
    Enumeration representing different types of documents.

    Attributes:
        VEN: Represents a "VEN" type document.
        PVEN: Represents a "PVEN" type document.
        OPPA: Represents an "OPPA" type document.
        POCD: Represents a "POCD" type document.
    """
    VEN = "VEN"
    PVEN = "PVEN"
    OPPA = "OPPA"
    POCD = "POCD"


class Sexo(Enum):
    """
    Enum representing gender categories.

    Attributes:
        M: String value "M", representing male gender.
        F: String value "F", representing female gender.
    """
    M = "M"
    F = "F"


class PersonaTelefono(BaseModel):
    """
    Represents an entry in the PersonaTelefono database.

    Attributes:
        nu_consecutivo_telefono (int): Consecutive phone number used for internal identification.
        st_telefono (int): The current status of the phone.
        cd_canal_informacion (int): Information channel code.
        cd_pais (int): Country code.
        tp_telefono (int): Type of phone number (e.g., mobile, landline).
        nu_area (int): Area code of the phone number.
        nu_telefono (int): The actual phone number.
    """
    nu_consecutivo_telefono: int
    st_telefono: int
    cd_canal_informacion: int
    cd_pais: int
    tp_telefono: int
    nu_area: int
    nu_telefono: int


class PersonaDireccion(BaseModel):
    """
    PersonaDireccion represents the address information of a person.

    Attributes:
        tp_via: Type of street (e.g., avenue, street).
        nm_calle: Name of the street.
        cd_pais: Country code.
        cd_provincia: Province code.
        cd_zona: Zone code.
        di_fiscal: Fiscal address indicator.
        tp_direccion: Type of address (e.g., home, work).
        cd_codigo_postal: Postal code.
        nu_piso: Floor number.
        di_completa: Complete address description.
        nu_consecutivo_direccion: Consecutive address number.
        di_postal: Postal address indicator.
        st_direccion: Address status.
        nu_puerta: Door number.
        nu_casa: House number.
        cd_municipio: Municipality code.
        nu_escalera: Stair number.
        cd_ciudad: City code.
        tp_vivienda: Type of housing.
        de_observacion: Observations about the address.
        di_cobro: Collection address indicator.
    """
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
    """
        PersonaEmail class represents the data structure for storing information about a person's email within a given system.

        Attributes:
            cd_canal_informacion (int): The code representing the information channel.
            st_email (int): The status of the email.
            de_email (str): The email address.
            tp_email (int): The type of email.
            nu_consecutivo_email (int): A sequential number associated with the email record.
    """
    cd_canal_informacion: int
    st_email: int
    de_email: str
    tp_email: int
    nu_consecutivo_email: int


class PersonaResponseBase(BaseModel):
    """
    A response model for handling persona (person) data including personal details, legal information, contacts, addresses, and more.

    Attributes:
        fe_inactivo: Date the person was marked inactive.
        cd_persona_representante_legal: Legal representative code for the person.
        de_actividades_ilicitas: Description of illicit activities associated with the person.
        in_rol_benef_preferencial: Indicates if the person has a preferential benefit role.
        cd_actividad_deportiva: Code representing the person's involvement in sports activities.
        nm_segundo_apellido: Person's second last name.
        in_bloquear_cobro: Indicates if payment collection is blocked for this person.
        nu_documento_seccion4: Section 4 document number for the person.
        nu_documento_seccion3: Section 3 document number for the person.
        cd_provincia_nacimiento: Code for the province of birth.
        cd_segmentacion_persona: Code for person segmentation.
        va_resultado_riesgo: Value representing the risk assessment result.
        nu_proximo_consec_tp_documento: Next consecutive document type number.
        nm_cheque: Name on the cheque.
        fe_ultima_verificacion: Date of the last verification.
        cd_persona_asesor_juridico: Legal advisor code.
        tp_empresa: Type of company.
        cd_ingreso_anual_dolar_princip: Principal annual income in dollars.
        tp_tax_identification: Type of tax identification.
        fe_fallecimiento: Date of death.
        persona_telefono: List of phone numbers associated with the person.
        cd_oficio_riesgo: Code for risk office.
        cd_empresa: Company code.
        nm_siglas_comercial: Commercial abbreviation.
        cd_empleado: Employee code.
        cd_pais_nacimiento: Code for country of birth.
        cd_estado_civil: Civil status code.
        nu_tax_identification: Tax identification number.
        tp_canal_informacion: Type of information channel.
        in_accionista_superior_a: Indicates if the person is a major shareholder.
        in_candidato_componente_excl: Indicates if the person is an excluded component candidate.
        in_incapacitado: Indicates if the person is incapacitated.
        in_vip: Indicates if the person is a VIP.
        nu_documento: Document number.
        in_pep: Indicates if the person is a politically exposed person.
        cd_sucursal_envio: Branch code for sending information.
        nm_primer_apellido: First last name.
        in_bloqueo_pago: Indicates if payment is blocked.
        fe_primera_verificacion: Date of first verification.
        in_inactivo: Indicates if the person is inactive.
        nm_apellido_casada: Married last name.
        in_residente_pais: Indicates if the person is a country resident.
        in_sujeto_obligado: Indicates if the person is a subject obligor.
        cd_ingreso_anual: Annual income code.
        de_observacion_inactivo: Observation notes for inactive status.
        fe_nacimiento: Date of birth.
        persona_direccion: List of addresses associated with the person.
        cd_causa_inactivo: Code for the cause of inactivity.
        persona_email: List of email addresses associated with the person.
        cd_persona: Unique person code.
        cd_entidad_envio: Sending entity code.
        de_justifica_renglon_prima: Justification for the premium line.
        de_ingreso_adicional: Description of additional income.
        cd_pais_residencia: Code for the country of residence.
        cd_usuario: User code.
        nm_primer_nombre: First name.
        cd_ciudad_nacimiento: Code for the city of birth.
        cd_envio: Sending code.
        de_observacion: General observation notes.
        in_persona_especial_fiscal: Indicates if the person is a special fiscal entity.
        cd_actividad: Activity code.
        cd_profesion: Profession code.
        cd_afinidad: Affinity code.
        cd_dependencia3: Third dependency code.
        di_verificador: Verifier indicator.
        cd_dependencia2: Second dependency code.
        cd_persona_agente_residente: Resident agent person code.
        cd_dependencia1: First dependency code.
        in_residente_accionista_eeuu: Indicates if the person is a US resident shareholder.
        nu_ideaseg: IDEAS number.
        nm_segundo_nombre: Second name.
        de_aviso_operaciones: Operations notice description.
        tp_documento: Type of document.
        nu_registro: Registration number.
        tp_persona: Person type.
        nu_ultimo_acuerdo_pago: Last payment agreement number.
        de_empresa: Company description.
        tp_riesgo_persona: Person risk type.
        in_lista_negra: Indicates if the person is on a blacklist.
        nu_rif: RIF number.
        cd_grupo_persona: Person group code.
        nu_endoso_formulario_cliente: Client form endorsement number.
        in_pago_exterior: Indicates if external payment is allowed.
        nu_tomo: TOMO number.
        cd_sector: Sector code.
        nm_zonarazonsocial: Zone/business name.
        nu_documento_seccion2: Section 2 document number for the person.
        nu_documento_seccion1: Section 1 document number for the person.
        cd_ocupacion: Occupation code.
        fe_vcto_registro_mercantil: Expiry date for mercantile registration.
        fe_ingreso_sistema: System entry date.
        in_actividades_ilicitas: Indicates if there are illicit activities.
        fe_registro: Registration date.
        cd_renglon_prima: Premium line code.
        cd_nacionalidad: Nationality code.
        cd_sexo: Sex code.
        nu_proximo_endoso: Next endorsement number.
        nm_razon_social: Business name.
        fe_vencimiento_documento: Document expiry date.
        cd_ingreso_anual_dolar_otra: Secondary annual income in dollars.
        de_act_economica_adicional: Description of additional economic activity.
    """
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
    """
        CreadaPersonaResponse class

        Represents the response data of a created person.

        Attributes:
            nm_zonarazonsocial (str): The legal name or trade name of the person.
            nu_documento (str): The document number of the person.
            tp_documento (str): The type of the document.
            cd_persona (int): The unique identifier of the person.
    """
    nm_zonarazonsocial: str
    nu_documento: str
    tp_documento: str
    cd_persona: int


class CoberturaResponse(BaseModel):
    """
    Represents the response model for the Cobertura API.

    Attributes:
        suma: An integer representing the sum or total amount involved.
        total_prima_bien: A float representing the total premium amount for the asset.
        prima: A float representing the amount of the premium.
        de_garantia: A string representing the guarantee description.
        comision: An integer representing the commission amount.
        cd_garantia: An integer representing the code or identification for the guarantee.
    """
    suma: int
    total_prima_bien: float
    prima: float
    de_garantia: str
    comision: int
    cd_garantia: int


class BienesResponse(BaseModel):
    """
    Class representing a response related to an asset (Bienes) with associated coverages.

    Attributes:
        nu_bien (int): The numeric identifier of the asset.
        coberturas (List[CoberturaResponse]): A list of coverage responses associated with the asset.
    """
    nu_bien: int
    coberturas: List[CoberturaResponse]


class CotizacionResponse(BaseModel):
    """
    class CotizacionResponse(BaseModel):
        de_plan_pago: str
            Description of the payment plan.
        mt_sig_cuota: float
            Amount for the next installment.
        mt_suma: int
            Total sum insured.
        nm_agente_bancario: str
            Name of the banking agent.
        cd_plan_pago: int
            Identifier code of the payment plan.
        nu_item: int
            Item number.
        mt_prima_pago: float
            Premium amount for the payment.
        bienes: List[BienesResponse]
            List of insured assets.
        de_plan: str
            Description of the insurance plan.
        in_seleccion: str
            Indicates the selection state.
        mt_prima_total: float
            Total premium amount.
        cd_moneda: int
            Currency code.
        nu_total_cuota: int
            Total number of installments.
        cd_entidad: int
            Identifier code of the entity.
        cd_plan: int
            Identifier code of the plan.
        nu_cotizacion: int
            Quotation number.
        cd_agente_bancario: str
            Code of the banking agent.
        nu_sec_estructura: str
            Structure sequence number.
    """
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
    """
    Represents a response message model.

    Attributes:
        id (int): The unique identifier for the message.
        mensaje (str): The content of the message.
    """
    id: int
    mensaje: str


class GarantiaResponse(BaseModel):
    """
    Class representing a warranty response.

    Attributes:
        mt_suma_aseg (int): The insured sum amount.
        mt_comision (int): The commission amount.
        de_garantia (str): The description of the warranty.
        cd_garantia (int): The warranty code.
        mt_prima (float): The premium amount.
    """
    mt_suma_aseg: int
    mt_comision: int
    de_garantia: str
    cd_garantia: int
    mt_prima: float


class CertificadoResponse(BaseModel):
    """
        A class used to represent a CertificadoResponse.

        Attributes:
            nu_convenio_pago (int): The payment agreement number.
            nu_certificado (int): The certificate number.
            nu_bien (int): The goods number.
            mt_prima_total (float): The total premium amount.
            cd_recibo (int): The receipt code.
            garantias (List[GarantiaResponse]): The list of guarantees.
            nu_orden_pago (str): The order payment number.
            nu_endoso (int): The endorsement number.
            de_bien (str): The description of the goods.
    """
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
    """
    Represents the response for an emission request.

    Attributes:
        de_plan (str): Description of the plan.
        nu_poliza (int): Policy number.
        nm_agente_bancario (str): Name of the banking agent.
        nu_secuencia_estructura (str): Sequence structure number.
        cd_moneda (int): Currency code.
        mensajes (List[MensajeResponse]): List of message responses.
        cd_entidad (int): Entity code.
        cd_plan (int): Plan code.
        cd_area (int): Area code.
        cd_agente_bancario (str): Banking agent code.
        certificado (List[CertificadoResponse]): List of certificate responses.
    """
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
    """
    Represents the response data for a policy installment (cuota) consultation.

    Attributes:
        nu_cuota (int): The installment number.
        fe_st_cuota (str): The status date of the installment.
        mt_pendiente (float): The pending amount.
        cd_status_cuota (int): The status code of the installment.
        mt_pendiente_sin_igtf (float): The pending amount without IGTF.
        mt_cuota (float): The total amount of the installment.
        de_status_cuota (str): The descriptive status of the installment.
        fe_vencimiento_cuota (str): The due date of the installment.
        tp_cuota (str): The type of installment.
        mt_pagado (int): The amount paid.
    """
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
    """
        MediadorConsultaPolizaResponse
        Represents the response model for a policy mediator consultation.

        Attributes:
            cd_mediador_especial (str): Special mediator code.
            nm_mediador_especial (str): Special mediator name.
            cd_mediador (int): Mediator code.
            cd_persona_mediador_especial (str): Special mediator person code.
            po_participacion_mediador (int): Mediator participation percentage.
            cd_persona_mediador (int): Mediator person code.
            nm_mediador (str): Mediator name.
            in_mediador_principal (int): Principal mediator indicator.
    """
    cd_mediador_especial: str
    nm_mediador_especial: str
    cd_mediador: int
    cd_persona_mediador_especial: str
    po_participacion_mediador: int
    cd_persona_mediador: int
    nm_mediador: str
    in_mediador_principal: int


class ReciboConsultaPolizaResponse(BaseModel):
    """
        ReciboConsultaPolizaResponse:
            Modelo que representa la respuesta de una consulta de recibo de póliza.

        Attributes:
            nu_convenio_pago (int): Número de convenio de pago.
            fe_emision_recibo (str): Fecha de emisión del recibo.
            de_status_recibo (str): Descripción del estado del recibo.
            fe_desde_recibo (str): Fecha de inicio de vigencia del recibo.
            cd_recibo (int): Código del recibo.
            fe_hasta_recibo (str): Fecha de fin de vigencia del recibo.
            tp_transaccion (int): Tipo de transacción.
            mt_prima (float): Monto de la prima.
            mt_igtf (float): Monto del impuesto sobre grandes transacciones financieras (IGTF).
            cuotas (List[CuotaConsultaPolizaResponse]): Lista de detalles de las cuotas asociadas al recibo.
            mt_recibo (float): Monto total del recibo.
            cd_status_recibo (int): Código del estado del recibo.
    """
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
    """
    CertificadoConsultaPolizaResponse is a model that represents the response of a policy inquiry containing
    various details about the insurance certificate and its related entities.

    Attributes:
        cd_persona_asegurada (int): Identifier for the insured person.
        des_producto (str): Description of the product.
        fe_proxima_facturacion (str): Date of the next billing cycle.
        de_plan_pago (str): Description of the payment plan.
        fe_desde_cert (str): Start date of the certificate.
        nu_certificado (int): Certificate number.
        cd_plan_pago (int): Identifier for the payment plan.
        nu_ultimo_convenio_pago (str): Number of the last payment agreement.
        de_status_cert (str): Description of the certificate's status.
        recibos (List[ReciboConsultaPolizaResponse]): List of receipt details related to the policy inquiry.
        fe_hasta_cert (str): End date of the certificate.
        nu_ultimo_endoso (int): Last endorsement number.
        cd_status_cert (int): Identifier for the certificate's status.
        cd_producto (int): Identifier for the product.
        fe_emision_certificado (str): Date of certificate issuance.
        mediadores (List[MediadorConsultaPolizaResponse]): List of mediators related to the policy.
        fe_ultimo_endoso (str): Date of the last endorsement.
    """
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
    """
        PolizaConsultaResponse
        A model representing the response of a policy consultation.

        Attributes:
            cd_persona_contratante (int): The code of the contracting person.
            cd_sucursal (int): The code of the branch.
            tp_contrato (str): The type of contract.
            nm_agente_bancario (str): The name of the banking agent.
            de_moneda (str): The description of the currency.
            tp_negocio (str): The type of business.
            certificados (List[CertificadoConsultaPolizaResponse]): A list of certificates for policy consultation.
            tp_facturacion (str): The type of billing.
            afinidad (str): The affinity.
            nu_poliza (int): The policy number.
            nu_secuencia_estructura (str): The sequence structure number.
            cd_moneda (int): The currency code.
            fe_emision_poliza (str): The policy issue date.
            cd_entidad (int): The code of the entity.
            cd_area (int): The code of the area.
            cd_agente_bancario (str): The code of the banking agent.
    """
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
    """
    Class representation for PolizasConsultaResponse which extends BaseModel.

    Attributes:
        polizas (List[PolizaConsultaResponse]): A list of PolizaConsultaResponse objects.
    """
    polizas: List[PolizaConsultaResponse]


class AnexoResponse(BaseModel):
    """
    AnexoResponse is a data model that represents the response details of an annex.

    Attributes:
        cd_persona_asegurada (str): The code of the insured person.
        nm_anexo (str): The name of the annex.
        nu_consecutivo_anexo (str): The consecutive number of the annex.
        nu_certificado (str): The certificate number.
        fe_exclusion (str): The date of exclusion.
        tp_inclusion_anexo (str): The type of inclusion of the annex.
        cd_producto (str): The product code.
        fe_inclusion (str): The date of inclusion.
        in_manual (str): Indicates if the data was entered manually.
        de_st_certificado (str): The description of the certificate status.
        cd_area_anexo (str): The code of the annex area.
        de_tp_inclusion_anexo (str): The description of the type of inclusion of the annex.
        nm_zonarazonsocial (str): The name of the social reason zone.
        nu_poliza (str): The policy number.
        de_entidad (str): The description of the entity.
        de_cd_area (str): The description of the area code.
        cd_entidad (str): The code of the entity.
        cd_anexo (str): The code of the annex.
        cd_area (str): The area code.
        de_producto (str): The description of the product.
        st_certificado (str): The status of the certificate.
        nu_endoso (str): The endorsement number.
    """
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
    """
    AnexosConsultaResponse serves as a response model for anexos (attachments) queries.

    Attributes:
        anexo (List[AnexoResponse]): List of AnexoResponse objects representing the attachments.
    """
    anexo: List[AnexoResponse]
