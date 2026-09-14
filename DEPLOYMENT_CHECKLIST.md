# Production Deployment Checklist

- [ ] Set a strong `GENESIS_JWT_SECRET` in the deployment secret store.
- [ ] Set `GENESIS_DATA_ROOT` to a persistent, access-controlled directory.
- [ ] Set `GENESIS_MAX_UPLOAD_BYTES` according to infrastructure limits.
- [ ] Configure production CORS origins instead of permissive development origins.
- [ ] Validate `/auth/register`, `/auth/login`, and `/auth/me` over HTTPS.
- [ ] Validate the complete `/v2` upload-to-report workflow with a test tenant.
- [ ] Confirm tenant A cannot access tenant B datasets.
- [ ] Confirm legacy routes return HTTP 410 after client migration.
- [ ] Configure backups and monitoring for the metadata database and dataset storage.
- [ ] Review residual placeholder analytics behavior before public launch.
