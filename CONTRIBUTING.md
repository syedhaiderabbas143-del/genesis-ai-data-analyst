# Contributing

1. Create a feature branch.
2. Do not commit secrets, local databases, generated reports, or customer data.
3. Run `python -m compileall -q .`.
4. Run `pytest -q` with a sufficiently long `GENESIS_JWT_SECRET`.
5. Open a pull request and wait for CI to pass.
