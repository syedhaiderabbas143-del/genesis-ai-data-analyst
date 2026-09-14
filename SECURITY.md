# Security Policy

## Reporting a vulnerability

Please do not open a public issue for security vulnerabilities. Contact the repository owner privately with reproduction steps, impact, and affected files.

## Secrets

Never commit `.env`, credentials, private keys, production databases, or real customer datasets. Use repository/environment secrets in deployment systems.

## Supported baseline

Pull requests must pass compilation and the automated test suite before merge.
