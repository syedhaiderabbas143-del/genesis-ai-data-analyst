# Architecture Migration

The application is being migrated from a monolithic `main.py` into:

- `api/routers`: HTTP endpoints
- `services`: business workflows
- `schemas`: request/response models
- `engines`: analytics and agent logic
- `security`: authentication, rate limiting, isolation, safe file paths

Migration should be incremental: one endpoint group at a time, with regression tests after each move.
