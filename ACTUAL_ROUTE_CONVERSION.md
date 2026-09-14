# Actual Route Conversion — Phase 7

Added tenant-scoped `/v2` routes while preserving legacy endpoints for regression-safe migration:

- `POST /v2/upload`
- `GET /v2/datasets`
- `DELETE /v2/datasets/{dataset_id}`
- `POST /v2/datasets/{dataset_id}/filter`
- `POST /v2/datasets/{dataset_id}/ask`

Every route requires a valid Bearer JWT and resolves data through `DatasetRepository` using the authenticated `sub` as owner. The old routes are intentionally retained until dashboard, forecasting, correlation, reporting and chart handlers are migrated.
