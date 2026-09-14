# Engine Integration Phase 2

This phase introduces a compatibility-safe facade for analytics engines.

## Migrated boundaries

- Ask workflow boundary
- Dashboard analytics boundary
- Correlation engine boundary
- Forecast engine boundary
- Root-cause engine boundary

## Legacy state policy

New code must receive a `pandas.DataFrame` loaded through the authenticated dataset repository. New services must not read or write the legacy module-level `latest_df`.

The legacy routes remain temporarily available for compatibility. Their complete removal requires endpoint-by-endpoint regression tests against the existing frontend.
