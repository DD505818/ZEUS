# ⚡ ZEUS°NXTLVL vX

ZEUS°NXTLVL vX is an elite-level, AI-driven trading system designed for rapid capital growth. This folder contains a Docker-based setup for running the backend API, frontend dashboard, analytics services, and automation tasks via Airflow.

## Usage

1. Populate the `.env` file with your configuration and API keys.
2. Build the Docker images and start the stack:

```bash
docker compose build
docker compose up -d
```

3. Access the services:
   - Frontend dashboard: http://localhost:3000
   - FastAPI backend: http://localhost:8000/docs
   - Airflow UI: http://localhost:8080
   - Metrics exporter: http://localhost:9100/metrics

This setup is intended for local development but mirrors a production architecture with Redis, PostgreSQL, and Qdrant.
