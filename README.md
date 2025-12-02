# Integration Seguros Mercantil (FastAPI)

Asistensi’s Integration for Seguros Mercantil. This service exposes versioned FastAPI endpoints that integrate with Seguros Mercantil APIs (quotations, policy issuance/consultation, payments, etc.) and an internal Pasarela de Pago module. It also provides a simple health check and interactive API docs.

Last updated: 2025-11-18 14:02 (local time)

## Overview

- API: FastAPI application wiring multiple versioned routers:
  - Integration_SM: v1, v2, v3, v4, v5
  - PasarelaPagoMS: v1, v2
- Entrypoint: `run.py` starts `uvicorn` serving `app.api.app:app` on port `9000`.
- Docs: Swagger UI at `GET /docs`. Health at `GET /health`.
- Configuration is loaded at import time from `.env` using Pydantic Settings.

## Tech stack

- Language: Python 3.12
- Frameworks/Libraries:
  - FastAPI, Pydantic v2
  - Uvicorn
  - Loguru (logging), PyMongo (optional logging sink)
  - HTTPX/Requests (HTTP clients)
- Package/dependency manager: `uv` (Astral)
- Tests: `pytest` (smoke tests included)

## Requirements

- Python 3.12+
- `uv` (installed automatically in Docker image; locally, install from https://docs.astral.sh/uv/)
- A `.env` file at the project root. For local development, copy the sample:
  - `cp .env.develop .env`

## Quickstart (local)

1) Install dependencies

```
uv sync --frozen --no-cache
```

2) Provide environment variables

```
cp .env.develop .env
# Edit .env as needed (see Configuration section below)
```

3) Run the API

```
python run.py
# or explicitly via uv
uv run --env-file .env python run.py
```

4) Verify

```
curl http://localhost:9000/health
# -> {"status": "ok"}

open http://localhost:9000/docs
```

## Running with Docker

Build and run with the default compose file (maps port 9000):

```
docker compose up --build
```

Environment-specific compose files are available:

- Dev/Test: `docker compose -f docker-compose_test.yml up --build`
- Staging: `docker compose -f docker-compose_staging.yml up --build`
- Prod: `docker compose -f docker-compose.yml up --build`

Notes:
- The container runs: `uv run --env-file .env python3 run.py`.
- Port 9000 is exposed. Logs are written to console and, when possible, to `logs/` (mounted by default in `docker-compose.yml`).

## Scripts and entry points

- Local entry point: `python run.py` (starts Uvicorn on port 9000). Reload is enabled unless `ENV` is `production` or `staging`.
- Uvicorn target: `app.api.app:app`
- No `make` or `poetry` scripts are defined. Package metadata is in `pyproject.toml` (managed by `uv`).

## Configuration (environment variables)

Configuration is loaded at import time from `.env` via `app/utils/v1/configs.py` and Pydantic Settings. Treat all variables as required. Do not hardcode secrets; use `.env`.

Known keys (names only; values must be provided via `.env`):

```
API_KEY_AUTH
SM_PRIMARY_KEY
SM_SECONDARY_KEY
SM_ENDPOINT
USER
APPLICATION
SUBSCRIPTION_KEY
ENV
ALLOWED_HOST
SUMA_ASEGURADA
SM_PRIMARY_PASARELA_KEY
SM_ENDPOINT_PASARELA_MS
SM_PRIMARY_SUSCRIPTION_KEY
SM_ENDPOINT_SUSCRIPCION
MID
MOCKUP
SM_ENDPOINT_NOTIFICACION_PAGO
SM_NOTIFICACION_PAGO_KEY
MONGO_URI
URL_ANULAR_POLIZA
API_KEY_ANULAR_POLIZA
```

Tips:
- For local development, start from `.env.develop` and adjust values as needed.
- Logging sinks are resilient: if `logs/` is not writable, logging falls back to console; if Mongo is unavailable, the Mongo logging sink is skipped without failing the app or tests.

## Testing

A minimal smoke suite exists under `tests/`.

One-time setup:

```
uv sync --frozen --no-cache
uv pip install pytest httpx
cp .env.develop .env    # ensure configuration exists; settings load at import time
```

Run tests:

```
python -m pytest -v
# or a specific file
python -m pytest tests/test_api.py -v
```

The suite currently covers:
- `GET /health` returns 200 and `{"status": "ok"}`
- `GET /docs` is reachable

## API surface

- `GET /health` → `{"status": "ok"}`
- `GET /docs` → Swagger UI
- Versioned routers are included under:
  - `/api/v1/sm`, `/api/v2/sm`, `/api/v3/sm`, `/api/v4/sm`, `/api/v5/sm`
  - `/api/v1/pasarela_pago_ms`, `/api/v2/pasarela_pago_ms`

Refer to `docs/ARCHITECTURE.md` and `docs/ARCHITECTURE_C4_3_COMPONENTS.md` for architecture details and runtime wiring.

## Project structure (selected)

```
app/
  api/
    app.py                 # FastAPI app, routers, /health, /docs
    v1/… v2/… v3/… v4/… v5/
      Integration_SM/
      PasarelaPagoMS/
  middlewares/
  schemas/
    v1/ v2/ v3/ v4/ v5/    # Versioned Pydantic models (do not mutate existing)
  utils/
    v1/ v2/ v3/ v4/ v5/    # Logging, configs, constants, etc.
docs/
tests/
run.py                      # Entrypoint (uvicorn)
pyproject.toml              # Managed by uv; dependencies and metadata
docker-compose*.yml
Dockerfile
```

## Development notes

- Code style: module/class/function docstrings with Args/Returns; explicit error handling; log contextual data.
- API versioning: do not mutate existing Pydantic models. Add new models under a new version and expose them via new routers.
- Configuration boundaries: treat all `Settings` fields as required via `.env`.

## CI/CD

Bitbucket Pipelines deploy by branch:
- `develop` → dev
- `staging` → staging
- `main` → prod

Suggested gates (see `docs/REPORT.md`): add ruff/black/mypy and expand unit tests (payload mappers/validators, regressions for known hotfixes) before deploy.

## License

TODO: Add license file and statement (e.g., MIT, Apache-2.0) or link to internal licensing policy.

## Maintenance TODOs

- Expand tests: payload mappers, validators, and key endpoints; add regression tests for known hotfixes.
- Add linting/formatting/type checks in CI (ruff, black, mypy).
- Document authentication expectations for protected routes (header name, example flows).
- Publish OpenAPI schema artifact if needed (e.g., `openapi.json`).
