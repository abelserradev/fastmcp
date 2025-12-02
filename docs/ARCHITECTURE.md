### Arquitectura — Integration Seguros Mercantil

Este documento describe la arquitectura a alto nivel del proyecto y provee un diagrama en formato Mermaid. Abra este archivo en un visor compatible con Mermaid (por ejemplo, GitHub, VS Code con la extensión adecuada, o el panel de vista previa de su IDE).

#### Visión general
- Framework: FastAPI (aplicación principal en `app/api/app.py`).
- Versionado de API: v1–v5 para `Integration_SM` y v1–v2 para `PasarelaPagoMS`.
- Esquemas: Pydantic en `app/schemas/**`.
- Utilidades transversales: configuración, constantes, logging (stdout/archivo/MongoDB), HTTP helper, plantillas de payload.
- Middlewares: CORS y GZip; verificación de API key como dependencia.
- Integraciones externas: Seguros Mercantil (productos/pólizas), Pasarela Pago MS, tasa BCV (cuando aplica), MongoDB para logs.

#### Diagrama (Mermaid)

```mermaid
flowchart TD
    %% Entradas
    subgraph Clients[Clientes]
        A1[Apps/Servicios internos]
        A2[Integradores externos]
    end

    %% FastAPI App y Middlewares
    A1 -->|HTTP| B[FastAPI App\napp/api/app.py]
    A2 -->|HTTP| B

    subgraph Middlewares[Middlewares]
        M1[CORS]
        M2[GZip]
        M3[API Key Verifier<br/>app/middlewares/verify_api_key.py]
    end
    B --> M1 --> M2 --> M3

    %% Routers por versión
    subgraph Routers[Routers por versión]
        direction TB
        subgraph R1[v1]
            R1a[Integration_SM\napp/api/v1/Integration_SM/app.py]
            R1b[PasarelaPagoMS\napp/api/v1/PasarelaPagoMS/app.py]
        end
        subgraph R2[v2]
            R2a[Integration_SM\napp/api/v2/Integration_SM/app.py]
            R2b[PasarelaPagoMS\napp/api/v2/PasarelaPagoMS/app.py]
        end
        subgraph R3[v3]
            R3a[Integration_SM]
        end
        subgraph R4[v4]
            R4a[Integration_SM]
        end
        subgraph R5[v5]
            R5a[Integration_SM<br/>últimos flujos / cotización global]
        end
    end

    M3 --> Routers

    %% Esquemas Pydantic
    subgraph Schemas[Esquemas - Pydantic]
        S1[app/schemas/v1/**]
        S2[app/schemas/v2/**]
        S3[app/schemas/v3/**]
        S4[app/schemas/v4/**]
        S5[app/schemas/v5/**]
    end

    R1a --> S1
    R1b --> S1
    R2a --> S2
    R2b --> S2
    R3a --> S3
    R4a --> S4
    R5a --> S5

    %% Utilidades y soporte transversal
    subgraph Utils[Utilidades / Cross-cutting]
        U1[Configs .env<br/>app/utils/v1/configs.py]
        U2[Constants\napp/utils/v1/constants.py]
        U3[LoggerSingletonDB<br/>app/utils/v2/LoggerSingletonDB.py]
        U4[MongoDBHandler + DB<br/>app/utils/v1/MongoDBHandler.py<br/>app/utils/v1/database.py]
        U5[SyncHttpx<br/>app/utils/v2/SyncHttpx.py]
        U6[Payload templates<br/>app/utils/v2..v5/payload_templates.py]
    end

    Routers --> U1
    Routers --> U2
    Routers --> U3
    U3 --> U4
    Routers --> U5
    Routers --> U6

    %% Servicios externos
    subgraph External[Servicios Externos]
        X1[Seguros Mercantil<br/>backend pólizas/cotizaciones]
        X2[Pasarela Pago MS]
        X3[BCV - tasa<br/>consulta cuando aplica]
        X4[MongoDB<br/>cuida_saludDB.logs_integration_ms]
    end

    U5 -->|HTTP| X1
    U5 -->|HTTP| X2
    U5 -->|HTTP| X3
    U4 -->|Logs| X4

    %% Ejecución
    subgraph Runtime[Ejecución]
        R0[run.py -> Uvicorn 0.0.0.0:9000\nreload en dev]
        D1[Dockerfiles + Compose\nEntornos: dev/staging/prod]
        CI[Bitbucket Pipelines\nDeploy por rama]
    end

    R0 --> B
    D1 --> R0
    CI --> D1
```

#### Notas de diseño
- Las rutas consumen esquemas Pydantic por versión, evitando romper compatibilidad entre iteraciones.
- La configuración se centraliza con `BaseSettings` (carga por `.env`) y se expone como constantes de uso directo.
- El logging utiliza Loguru con sinks a stdout, archivo (rotación/retención) y MongoDB mediante un handler dedicado.
- `SyncHttpx` provee un helper sincrónico para llamadas HTTP salientes a los servicios externos.
- Las plantillas/mapeadores de payload permiten construir requests acordes a cada versión/endpoint externo.
- Los middlewares aplican CORS/GZip; la verificación de API Key se inyecta como dependencia a nivel de router/endpoint.

#### Cómo ejecutar
- Local: `python run.py` (puerto 9000; reload en desarrollo).
- Docker: `docker compose up --build` (usar archivos específicos por entorno).
