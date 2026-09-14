# Advanced Analytics Route Migration

Added tenant-scoped endpoints:

- `GET /v2/datasets/{dataset_id}/dashboard`
- `POST /v2/datasets/{dataset_id}/correlation`
- `POST /v2/datasets/{dataset_id}/forecast`
- `GET /v2/datasets/{dataset_id}/report`

Every endpoint resolves the dataset through the authenticated owner and dataset ID. The legacy global-state routes remain unchanged for compatibility and must be deprecated after frontend migration.
