# Security Hardening Phase 1

Implemented in this candidate:

- Replaced wildcard CORS with environment-configured allowed origins.
- Restricted CORS methods and headers instead of allowing everything.
- Added `GET /health` liveness endpoint.
- Added `.env.example` for local configuration.
- Added `.env`, key, certificate, and upload-directory exclusions to `.gitignore`.
- Ensured required runtime dependencies include NumPy, SciPy, Pydantic, and psutil.

## Run

```powershell
$env:GENESIS_ALLOWED_ORIGINS="http://localhost:8000,http://127.0.0.1:8000"
python -m uvicorn main:app --reload
```

## Remaining high-priority work

- Add authentication and authorization.
- Remove module-level shared DataFrame state.
- Make generated charts private and user/job scoped.
- Add upload rate limits and stronger content validation.
- Split the monolithic `main.py` into routers, services, schemas, and engines.
