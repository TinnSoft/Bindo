.PHONY: help init-db upgrade-db

help:
	@echo "Targets: init-db upgrade-db run"

init-db:
	@echo "Initializing DB (alembic upgrade head)"
	alembic -c alembic.ini upgrade head

upgrade-db:
	alembic -c alembic.ini revision --autogenerate -m "auto"

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
