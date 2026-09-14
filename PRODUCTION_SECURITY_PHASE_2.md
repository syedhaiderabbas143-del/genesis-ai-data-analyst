# Production Security Phase 2

Implemented a production-oriented identity and tenancy foundation without replacing the existing analytics engine in one risky refactor.

## Included
- JWT bearer identity with signed tokens.
- Persistent SQLite session records with JTI revocation.
- PBKDF2-HMAC-SHA256 password hashing using the Python standard library.
- User roles (`analyst` foundation + reusable role dependency).
- User-owned dataset and chart ownership tables/helpers.
- Redis-backed rate limiting when `REDIS_URL` and the optional `redis` package are configured; local in-memory fallback otherwise.
- Authentication endpoints: `/auth/register`, `/auth/login`, `/auth/me`, `/auth/logout`.

## Environment
- `GENESIS_JWT_SECRET`: required for JWT operations; minimum 32 characters.
- `GENESIS_SECURITY_DB`: optional SQLite path.
- `REDIS_URL`: optional Redis connection URL.

## Important migration boundary
The existing analytics routes still contain legacy global state. The new ownership helpers are ready, but every dataset/chart-producing endpoint must be migrated to require `current_user` and an owned dataset/chart identifier before this can be called fully multi-tenant production-ready.

## Production checklist
- Put the API behind HTTPS/TLS.
- Store secrets in a managed secret store/environment, never Git.
- Use managed PostgreSQL instead of SQLite for multi-instance deployments.
- Use Redis for distributed rate limiting.
- Add refresh-token rotation or short-lived access tokens with secure refresh sessions.
- Add account recovery, lockout/brute-force protection, CSRF protection if cookie auth is used, audit logging, and security monitoring.
