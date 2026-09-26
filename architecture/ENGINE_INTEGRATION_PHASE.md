# Advanced Engine Integration + Legacy State Removal

## Phase status

This phase introduces a controlled service boundary for tenant-scoped analytics.
It does **not** claim that every legacy route has already been rewritten.

## Changes

- Added `services/engine_registry.py` with an allow-listed canonical engine registry.
- Added `services/tenant_analytics_service.py` to load datasets only through the owner-aware repository.
- Removed no legacy files and did not alter the original project archive.
- Prevented arbitrary module imports through the engine resolver.
- Kept DataFrame state inside request/service scope instead of adding new globals.

## Migration contract

```python
service = TenantAnalyticsService(repository)
frame = service.load_owned_frame(current_user.id, dataset_id)
```

A route should never accept a filesystem path or read a global `latest_df`.

## Remaining work

1. Replace each legacy route body with calls to `TenantAnalyticsService`.
2. Move chart generation behind an owner-checked service.
3. Add request/response schemas for each analytics operation.
4. Remove legacy globals only after route-by-route regression tests pass.
5. Add integration tests for cross-user access, engine failures, and concurrent requests.
