# Makefile for Swakopmund Municipality Public Safety Service

.PHONY: help install dev test lint clean build up down logs

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Run development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8686

test: ## Run tests
	pytest -v --cov=app --cov-report=term-missing

test-watch: ## Run tests in watch mode
	pytest-watch

lint: ## Run linting
	flake8 app tests
	black --check app tests
	isort --check-only app tests

format: ## Format code
	black app tests
	isort app tests

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f test.db

build: ## Build Docker image
	docker build -t public-safety-service:latest .

up: ## Start services with Docker Compose
	docker-compose up -d --build

down: ## Stop services
	docker-compose down

logs: ## View logs
	docker-compose logs -f

shell: ## Open shell in running container
	docker-compose exec public_safety_service /bin/bash

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U postgres -d public_safety_db

setup-env: ## Copy environment template
	cp env.example .env
	@echo "Please edit .env file with your configuration"

migrate: ## Run database migrations (if using Alembic)
	alembic upgrade head

seed: ## Seed database with sample data
	python scripts/seed_data.py

backup-db: ## Backup database
	docker-compose exec postgres pg_dump -U postgres public_safety_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Restore database from backup (usage: make restore-db BACKUP_FILE=backup.sql)
	docker-compose exec -T postgres psql -U postgres -d public_safety_db < $(BACKUP_FILE)

production-build: ## Build for production
	docker build -f Dockerfile.prod -t public-safety-service:prod .

security-scan: ## Run security scan
	safety check
	bandit -r app/

performance-test: ## Run performance tests
	locust -f tests/performance/locustfile.py 