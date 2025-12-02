### Integration Seguros Mercantil — Project‑specific developer notes

This file captures concrete, project‑specific practices verified against the current repository and the docs in `docs/`. Audience: advanced developers.

Updated: 2025‑11‑18 13:48 local time

#### Build / configuration

- Runtime: Python 3.12. Dependency manager: `uv` (see `pyproject.toml`, `uv.lock`). Entrypoint: `run.py` → `uvicorn app.api.app:app` (port 9000; reload enabled unless `ENV` is `production`/`staging`).
- Central app: `app/api/app.py` wires routers for v1–v5 (`Integration_SM`) and v1–v2 (`PasarelaPagoMS`). It exposes `GET /health` and `GET /docs`.
- Settings: `app/utils/v1/configs.py` loads from `.env` at import time. Provide `.env` before running or testing. For local work, copy one of the provided envs and adjust:
  - `cp .env.develop .env` (or adapt from `.env.staging`). Keys include `API_KEY_AUTH`, `SM_*`, `MONGO_URI`, `ENV`, etc. See `Settings` class for full list.

Local run

1. Install dependencies:
   - `uv sync --frozen --no-cache`
2. Prepare env vars:
   - `cp .env.develop .env` and edit as needed.
3. Start API:
   - `python run.py`
   - Verify: `curl http://localhost:9000/health` → `{"status":"ok"}`

Docker

- Default: `docker compose up --build` (see `docker-compose.yml`).
- Env specific:
  - Dev/Test: `docker compose -f docker-compose_test.yml up --build`
  - Staging: `docker compose -f docker-compose_staging.yml up --build`
  - Prod: `docker compose -f docker-compose.yml up --build`

#### Testing

What exists now

- Tests live in `tests/`. A minimal smoke suite is present: `tests/test_api.py` covering `GET /health` and `GET /docs`.
- Verified on 2025‑11‑18: `2 passed` with pytest 9.0.1 under Python 3.12.3.

One‑time test setup

1. App deps: `uv sync --frozen --no-cache`
2. Testing tools: `uv pip install pytest httpx`
3. Ensure `.env` is present (see above). Settings are loaded at import time and logs are emitted.

Run tests

- All: `python -m pytest -v`
- Specific file: `python -m pytest tests/test_api.py -v`

Creating new tests

- Place files under `tests/` named `test_*.py`. Use FastAPI’s `TestClient`:

```python
from fastapi.testclient import TestClient
from app.api.app import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
```

- Authenticated example: include the API key header expected by middlewares/dependencies (adjust header name according to implementation):

```python
from fastapi.testclient import TestClient
from app.api.app import app

client = TestClient(app)

headers = {"X-API-Key": "test_api_key"}
resp = client.get("/api/v1/sm/protected", headers=headers)
assert resp.status_code in (200, 401, 403)
```

Notes and caveats (validated)

- Logging sinks are best‑effort to support CI and read‑only FS:
  - `app/utils/v1/LoggerSingleton.py` and `app/utils/v2/LoggerSingletonDB.py` now fall back to console if `logs/` cannot be created/written, and will skip Mongo sink if it cannot be set up. This prevents test collection failures due to `PermissionError` on `logs/YYYY-MM-DD.log`.
  - If you require file logs in CI, ensure `logs/` is writable or mount a volume. Otherwise, console logging is sufficient for tests.
- Mongo sink: with no Mongo available, you may see warnings like “MongoDB logging disabled (setup failed)” or a teardown message about a closed client. They are non‑fatal.

#### Additional development information

- Architecture: see `docs/ARCHITECTURE.md` and `docs/ARCHITECTURE_C4_3_COMPONENTS.md` for C4 view and runtime wiring. `docs/REPORT.md` lists follow‑ups (tests for payload mappers/validators, regression checks for known hotfixes, linters/type checks in CI).
- Code style: follow current docstring practice (module/class/function docstrings with Args/Returns), keep error handling explicit, and log contextual data (external status codes, request identifiers).
- API versioning: do not mutate existing Pydantic models. Add new models under `app/schemas/v{N}` and route changes through new versioned routers.
- Configuration boundaries: treat all `Settings` fields as required via `.env`. Never hardcode environment‑specific or secret values.
- Running in Docker/CI: expose port 9000; pass `.env` via secrets/variables. If you experience file logging permission issues, rely on console logs.

#### CI/CD

- Bitbucket Pipelines deploy by branch: `develop` → dev, `staging` → staging, `main` → prod. Incorporate unit tests and (optionally) ruff/black/mypy steps as pre‑deploy gates as recommended in `docs/REPORT.md`.

#### Quick checklist

- [ ] `uv sync --frozen --no-cache`
- [ ] `.env` present (e.g., from `.env.develop`)
- [ ] `python run.py` → `/health` returns 200
- [ ] `uv pip install pytest httpx` and `python -m pytest -v` → smoke tests pass
- [ ] For new features, add tests under `tests/` and avoid real external calls by mocking HTTP/Mongo