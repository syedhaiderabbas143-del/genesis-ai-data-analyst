# Deep Security + Architecture Review

## Executive verdict

**Status: NOT production-ready; suitable as a portfolio/development candidate after hardening.**

The application imports successfully and exposes a large FastAPI surface, but the current design is a monolithic API with global in-memory state and broad cross-origin access. The public candidate contains no detected obvious hard-coded secrets in the scanned source set.

## Findings

### Critical / high priority

1. **Wildcard CORS with credentials**
   - `main.py` configures `allow_origins=["*"]` and `allow_credentials=True`.
   - Risk: unsafe cross-origin policy and accidental exposure when authentication/cookies are introduced.
   - Fix: use an explicit allowlist from environment configuration; set credentials only when required.

2. **No visible authentication/authorization layer**
   - The reviewed `main.py` contains no obvious JWT, bearer-token, login, or authorization enforcement terms.
   - Risk: any reachable client may call the API unless protected by an external reverse proxy.
   - Fix: add authentication, authorization, per-user dataset isolation, and endpoint-level permissions before deployment.

3. **Global mutable dataset state**
   - `latest_df = None` and mutable audit/version lists are module-level state.
   - Risk: users can overwrite one another's data; race conditions and data leakage are possible with concurrent users or multiple workers.
   - Fix: use request/session/job IDs and isolated storage; avoid process-global DataFrames.

4. **Large monolithic `main.py`**
   - `main.py` is approximately 22k lines.
   - Risk: difficult review, testing, dependency management, merge conflict resolution, and security auditing.
   - Fix: split into routers, services, schemas, security, storage, analytics engines, and background jobs.

### Medium priority

5. **Broad API surface**
   - The app exposes approximately 72 route handlers in the public candidate.
   - Risk: larger attack surface and inconsistent validation/error behavior.
   - Fix: document each route, apply shared validation, authentication, rate limits, and consistent response models.

6. **File-upload attack surface**
   - CSV/XLSX ingestion is central to the app.
   - Required hardening: maximum request size at reverse proxy and application layers, MIME/content validation, decompression-bomb protection, filename normalization, isolated temporary directories, malware scanning where appropriate, and cleanup/retention policies.

7. **Generated-file serving**
   - The app mounts a charts directory as static content.
   - Risk: accidental publication of sensitive charts or filenames if generated output is not isolated per user/job.
   - Fix: private object/file storage with authorization checks, opaque IDs, and expiration.

8. **Dependency reproducibility**
   - Requirements are present but unpinned.
   - Fix: use a lock/constraints file, automated dependency vulnerability scanning, and regular upgrades.

### Architecture quality observations

- The project has strong feature breadth: profiling, quality, cleaning, charts, correlation, forecasting, anomaly/outlier analysis, root-cause analysis, recommendations, reporting, and multi-agent experiments.
- The codebase also shows signs of organic growth: duplicated engines, overlapping agent responsibilities, backup variants, and naming collisions.
- A modular architecture should establish one canonical implementation per capability and one orchestration entry point.

## Recommended target architecture

```text
app/
  main.py                 # application factory only
  api/
    routers/              # upload, profiling, analytics, reports
    dependencies.py       # auth, request context, limits
  core/
    config.py             # environment settings
    security.py           # auth, permissions, secrets handling
    logging.py
  schemas/                # Pydantic request/response models
  services/
    ingestion_service.py
    profiling_service.py
    analytics_service.py
    reporting_service.py
  engines/                # one canonical engine per capability
  storage/                # dataset/job/output persistence
  workers/                # background jobs for expensive analysis
  tests/
frontend/
sample_data/
docs/
```

## Priority remediation sequence

1. Replace wildcard CORS with an explicit environment-based allowlist.
2. Add authentication and per-user/per-job isolation.
3. Remove global DataFrame and global audit/version state.
4. Add upload limits, safe temporary storage, cleanup, and output authorization.
5. Split `main.py` into routers/services/schemas.
6. Remove or archive duplicate/backup modules and rename collisions.
7. Add automated tests for auth, tenant isolation, uploads, path traversal, oversized files, and error codes.
8. Pin dependencies and add CI security checks.
9. Add `/health` and `/ready` endpoints with non-sensitive status information.
10. Publish only the reviewed public subset; keep proprietary core and real datasets private.

## Publication decision

The candidate can be used for recruiter review as a **development/portfolio build**, but it should not be advertised as a secure production platform until the high-priority items above are implemented.
