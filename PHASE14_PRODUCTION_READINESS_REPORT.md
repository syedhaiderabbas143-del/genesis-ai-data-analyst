# Phase 14 — Production Readiness + Final Integration Validation

## Scope

Phase 14 validates the production boundary after legacy-route decommissioning:

- Python compilation of the complete project.
- Full pytest regression suite.
- FastAPI application import and route inventory.
- Authentication route presence.
- Tenant `/v2` dataset and advanced analytics route presence.
- Legacy decommission switch remains isolated from `/v2` routes.
- Required production environment controls are documented.

## Validation commands

```bash
python -m compileall -q .
GENESIS_JWT_SECRET=$(python -c "print('x'*40)") PYTHONPATH=. pytest -q
```

## Result

- Python compilation: **PASS**
- Regression suite: **17 passed, 1 skipped** before Phase 14 additions
- Phase 14 additions: **5 passed**
- Combined suite: **22 passed, 1 skipped**

## Production configuration controls

- `GENESIS_JWT_SECRET` must be a strong, non-default secret.
- `GENESIS_DISABLE_LEGACY_ROUTES=true` enables retirement responses for legacy paths.
- `GENESIS_MAX_UPLOAD_BYTES` controls upload size.
- `/v2` endpoints remain the supported tenant-scoped API surface.

## Remaining operational step

Run the application behind the intended production reverse proxy and execute authenticated HTTP tests against the deployed environment. This local validation does not claim cloud deployment or external infrastructure validation.
