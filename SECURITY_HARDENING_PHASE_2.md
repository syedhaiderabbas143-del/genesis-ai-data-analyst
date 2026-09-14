# Security Hardening Phase 2

## Implemented foundation

- `security/auth.py`: optional API-key dependency. Enable with `GENESIS_API_KEY`.
- `security/rate_limit.py`: thread-safe in-process rate limiter foundation.
- `security/storage.py`: owner/job-scoped dataset session store to replace shared global DataFrames in future route migration.
- `security/charts.py`: path-safe, owner-scoped chart path helper.
- `architecture/`: reserved for router/service/schema extraction in the next migration step.

## Important limitation

This phase adds the security building blocks without rewriting the large legacy `main.py` in-place. Existing routes still use legacy global state until they are migrated route-by-route. Do not treat this package as production-ready.

## Enable API key

PowerShell:

```powershell
$env:GENESIS_API_KEY = "replace-with-a-long-random-secret"
```

Use the `require_api_key` dependency on protected routes. Never commit the real key.

## Production recommendation

Use Redis or an API gateway for distributed rate limiting, a real identity provider/JWT system for users, and database/object storage for tenant-isolated datasets and charts.
