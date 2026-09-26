# Genesis AI Data Analyst

A portfolio-oriented AI Data Analyst application built with Python, FastAPI, Pandas, NumPy, SciPy, Matplotlib, and Excel/CSV processing.

## Capabilities

- CSV/XLSX upload and validation
- Dataset profiling and statistics
- Data-quality scanning and cleaning workflows
- Interactive dashboard chart generation
- Correlation and matrix analysis
- Trend/time-series analysis and forecasting workflows
- Outlier/anomaly analysis
- Root-cause analysis and recommendations
- Multi-agent orchestration experiments
- API documentation through FastAPI Swagger UI

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Data and privacy

This public candidate contains only a small synthetic sample dataset. Private datasets, generated exports, charts, virtual environments, caches, logs, and credentials are intentionally excluded. Never commit API keys, passwords, tokens, customer data, or production exports.

## Security status

This is a development/portfolio build, not a production deployment. Before production use, add authentication, authorization, rate limiting, audit logging, stricter CORS, secure file storage, and dependency/version scanning.

## Copyright

This repository is shared for portfolio and review purposes. No open-source license is granted unless a license file is explicitly added by the owner. Public Git hosting cannot prevent copying; sensitive or proprietary components should remain private.


## Advanced tenant-scoped analytics

Use the `/v2/datasets/{dataset_id}/...` endpoints for dashboard, correlation, forecast, and report operations. All require the authenticated user and an owned dataset ID.

## Public Repository Notice

This repository is a public portfolio release of Genesis AI Data Analyst. Runtime databases, Python cache files, credentials, and local/generated runtime artifacts are intentionally excluded from the public release.

### Project Positioning
Genesis AI Data Analyst is an AI-assisted analytics platform for Excel/CSV workflows, including data profiling, quality/cleaning, statistical analysis, correlation, trend analysis, forecasting, root-cause analysis, recommendations, dashboards, and analytical question answering.

The project should be evaluated as a portfolio engineering project. Public documentation distinguishes implemented capabilities from future roadmap work; it does not claim that the system literally replaces or possesses a human analyst's years of professional experience.

### Security
Do not place real API keys, passwords, tokens, production databases, customer data, or private datasets in this repository. Configure secrets through environment variables when running locally.

### Ownership
Copyright (c) 2026 Haider Abbas. All rights reserved. See `LICENSE`.

