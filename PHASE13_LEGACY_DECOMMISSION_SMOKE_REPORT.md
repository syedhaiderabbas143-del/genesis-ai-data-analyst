# Phase 13 — Legacy Route Decommission + Live API Smoke Testing

## Scope

- Added an opt-in legacy endpoint retirement policy.
- When `GENESIS_DISABLE_LEGACY_ROUTES=true`, pre-v2 endpoints return HTTP 410 with guidance to use `/v2`.
- `/v2` routes remain available and are not matched by the legacy policy.
- Added regression coverage for route presence, tenant authentication dependencies, and decommission behavior.

## Operational rollout

1. Deploy with `GENESIS_DISABLE_LEGACY_ROUTES=false` during compatibility validation.
2. Validate all clients use `/v2` endpoints.
3. Set `GENESIS_DISABLE_LEGACY_ROUTES=true` in the production environment.
4. Monitor HTTP 410 responses and remove the compatibility code after client migration.

## Smoke-test status

The included suite validates the route policy and API route wiring without requiring external services. A full network-level smoke test should be run against the deployed server with a configured JWT secret and API key.
