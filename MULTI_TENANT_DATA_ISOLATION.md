# Multi-Tenant Data Isolation

## Goal

Every dataset, chart, report, and analysis job must be owned by an authenticated
`user_id` (tenant). A request must never select a resource by ID alone.

## Required request flow

1. Validate the JWT and resolve `request.state.user_id`.
2. Require a `dataset_id`/`resource_id` in the request.
3. Resolve the resource through an ownership check:
   `get_owned(user_id, resource_type, resource_id)`.
4. Execute analytics only against the authorized resource.
5. Store generated charts/reports under the owner-scoped path.
6. Never use a module-level `latest_df` as the source of truth.

## Migration rule for legacy routes

Legacy endpoints should be migrated one at a time:

- `/upload`: create a dataset resource owned by the authenticated user.
- `/ask`: require `dataset_id`; load only that user's dataset.
- `/filter`: require `dataset_id`; never read shared global state.
- dashboard/forecast/correlation/report routes: require and verify `dataset_id`.
- chart endpoints: verify chart ownership before serving a file.

## Storage layout

```text
storage/
  <user_id>/
    datasets/<dataset_id>/
    charts/<chart_id>/
    reports/<report_id>/
```

The current implementation provides the ownership registry and confined-path
primitive. Full replacement of legacy global state must be completed route by
route and verified with cross-tenant tests before production deployment.
