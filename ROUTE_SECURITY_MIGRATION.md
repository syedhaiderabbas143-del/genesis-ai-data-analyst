# Route Security Migration

Phase 2 route migration adds opt-in protection for sensitive endpoint families:

- `/upload`
- `/ask`
- `/filter`
- `/dashboard`
- `/charts`
- analytics/reporting routes such as `/correlation`, `/forecast`, and `/report`

## Enable locally

PowerShell:

```powershell
$env:GENESIS_API_KEY = "use-a-long-random-secret"
$env:GENESIS_SECURITY_ENFORCED = "true"
python -m uvicorn main:app --reload
```

Send the key using the `X-API-Key` header. The middleware is opt-in so existing local development remains backward compatible. Before production, replace the single shared API key with per-user identity, persistent sessions, and a distributed rate limiter.
