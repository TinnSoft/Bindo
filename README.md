BINDO - MVP

This repository contains a minimal scaffold for the BINDO MVP.

Services:
- api: FastAPI backend
- web: Quasar (Vue 3 + TS) frontend
- postgres: PostgreSQL
- redis: Redis for Celery

Quickstart (development):

1) Copy `.env.example` to `.env` and fill values (OPENAI_API_KEY, DATABASE_URL)

2) Start services with Docker Compose:

```bash
docker compose up --build
```

3) API will be available at `http://localhost:8000` and web at `http://localhost:8080`

Notes:
- This is initial scaffolding: models, basic endpoints and Celery task stub are present.
- Next steps: implement migrations, full endpoints, LLM parsing logic, and frontend polish.
