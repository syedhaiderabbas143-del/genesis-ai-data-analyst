# Public GitHub Publication Checklist

- [ ] Review the selected Python files and remove proprietary logic that should remain private.
- [ ] Confirm no `.env`, credentials, API keys, private keys, customer data, or production exports are present.
- [ ] Keep real datasets, charts, reports, and generated files out of Git.
- [ ] Replace wildcard CORS with an explicit frontend origin before deployment.
- [ ] Add authentication and authorization before exposing the API publicly.
- [ ] Pin dependency versions after testing in a clean virtual environment.
- [ ] Run syntax, import, endpoint, and security tests.
- [ ] Publish only after reviewing the final diff.
