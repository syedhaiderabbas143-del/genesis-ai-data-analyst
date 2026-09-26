# Dataset Repository + Route Migration

Implemented a persistent SQLite metadata registry and owner-scoped CSV storage. Every dataset read, list, and delete operation requires the authenticated `owner_id`.

## Route contract

Protected routes must receive `current_user_id` from JWT/session authentication and a client-supplied `dataset_id`. They must load data only through:

```python
record, frame = dataset_for_request(repo, current_user_id, dataset_id)
```

Do not accept arbitrary filesystem paths and do not use a shared module-level `latest_df`.

## Required route wiring

- `/upload`: create a repository record and return `dataset_id`.
- `/ask`, `/filter`, dashboard, forecast, correlation and report routes: require `dataset_id`.
- Chart/report artifacts: use the same owner and dataset scope.
- Add cleanup for expired datasets and orphaned files.

CSV support requires `pyarrow` or `fastparquet`.
