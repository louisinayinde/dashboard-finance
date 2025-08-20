# Makefile for Dashboard Finance Project
# Usage: make <command>

.PHONY: help install install-dev install-test install-prod clean test test-unit test-integration test-e2e test-cov lint format type-check docker-build docker-up docker-down docker-logs docker-shell logs setup-db migrate seed logs

# Default target
help:
	@echo "Dashboard Finance - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  install-test     Install test dependencies"
	@echo "  install-prod     Install production dependencies"
	@echo ""
	@echo "Development:"
	@echo "  run              Run the application in development mode"
	@echo "  run-prod         Run the application in production mode"
	@echo "  celery-worker    Start Celery worker"
	@echo "  celery-beat      Start Celery beat scheduler"
	@echo "  celery-flower    Start Celery flower monitoring"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-e2e         Run end-to-end tests only"
	@echo "  test-cov         Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting (flake8)"
	@echo "  format           Format code (black + isort)"
	@echo "  type-check       Run type checking (mypy)"
	@echo "  check-all        Run all code quality checks"
	@echo ""
	@echo "Database:"
	@echo "  setup-db         Setup database (create, migrate, seed)"
	@echo "  migrate          Run database migrations"
	@echo "  seed             Seed database with sample data"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build     Build Docker images"
	@echo "  docker-up        Start all Docker services"
	@echo "  docker-down      Stop all Docker services"
	@echo "  docker-logs      Show Docker logs"
	@echo "  docker-shell     Open shell in app container"
	@echo ""
	@echo "Utilities:"
	@echo "  clean            Clean Python cache and build files"
	@echo "  logs             Show application logs"
	@echo "  shell            Open Python shell with app context"

# Installation
install:
	pip install -r requirements/base.txt

install-dev:
	pip install -r requirements/development.txt

install-test:
	pip install -r requirements/test.txt

install-prod:
	pip install -r requirements/production.txt

# Development
run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run-prod:
	gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

celery-worker:
	celery -A celery_app worker --loglevel=info --concurrency=2

celery-beat:
	celery -A celery_app beat --loglevel=info

celery-flower:
	celery -A celery_app flower --port=5555

# Testing
test:
	pytest

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-e2e:
	pytest tests/e2e/ -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Code Quality
lint:
	flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503

format:
	black app/ tests/ --line-length=88
	isort app/ tests/ --profile=black --line-length=88

type-check:
	mypy app/ --ignore-missing-imports

check-all: lint format type-check
	@echo "All code quality checks passed!"

# Database
setup-db:
	@echo "Setting up database..."
	python scripts/db/setup.py

migrate:
	alembic upgrade head

seed:
	python scripts/db/seed.py

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec app bash

# Utilities
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/

logs:
	tail -f logs/app.log

shell:
	python -c "from app.core.database import engine; from app.models.database import Base; Base.metadata.create_all(bind=engine)"
	python -i -c "from app.core.database import SessionLocal; from app.models.database import *; db = SessionLocal()"

# Pre-commit hooks
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

# Monitoring
monitoring-up:
	docker-compose up -d prometheus grafana

monitoring-logs:
	docker-compose logs -f prometheus grafana

# Production deployment
deploy-staging:
	@echo "Deploying to staging environment..."
	# Add your staging deployment commands here

deploy-production:
	@echo "Deploying to production environment..."
	# Add your production deployment commands here

# Backup and restore
backup-db:
	@echo "Creating database backup..."
	docker-compose exec postgres pg_dump -U dashboard_user dashboard_finance > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:
	@echo "Restoring database from backup..."
	@read -p "Enter backup file name: " backup_file; \
	docker-compose exec -T postgres psql -U dashboard_user -d dashboard_finance < $$backup_file
