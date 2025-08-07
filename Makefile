# Makefile for Product Management API

.PHONY: help install test test-unit test-integration lint format clean build run docker-build docker-run docker-stop docker-logs migrate migrate-up migrate-down migrate-status create-migration migrate-to

# Default target
help:
	@echo "Available commands:"
	@echo "  install        - Install dependencies in virtual environment"
	@echo "  activate       - Show how to activate virtual environment"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code with black"
	@echo "  clean          - Clean up generated files"
	@echo "  build          - Build Docker image"
	@echo "  run            - Run application locally"
	@echo "  docker-build   - Build Docker containers"
	@echo "  docker-run     - Start Docker containers"
	@echo "  docker-stop    - Stop Docker containers"
	@echo "  docker-logs    - Show Docker logs"
	@echo "  migrate        - Run database migrations"
	@echo "  migrate-up     - Apply database migrations"
	@echo "  migrate-down   - Rollback database migrations"
	@echo "  migrate-status - Show current migration status"
	@echo "  migrate-to     - Migrate to specific revision (usage: make migrate-to REV=<revision>)"
	@echo "  create-migration - Create a new migration file"

# Virtual environment
VENV_NAME = venv
VENV_BIN = $(VENV_NAME)/bin
VENV_PYTHON = $(VENV_BIN)/python
VENV_PIP = $(VENV_BIN)/pip

# Install dependencies
install: $(VENV_NAME)
	$(VENV_PIP) install -r requirements.txt

# Create virtual environment
$(VENV_NAME):
	python3 -m venv $(VENV_NAME)
	$(VENV_PIP) install --upgrade pip

# Activate virtual environment (for manual use)
activate:
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_BIN)/activate"

# Run all tests
test: $(VENV_NAME)
	$(VENV_PYTHON) -m pytest

# Run unit tests only
test-unit: $(VENV_NAME)
	$(VENV_PYTHON) -m pytest tests/unit/

# Run integration tests only
test-integration: $(VENV_NAME)
	$(VENV_PYTHON) -m pytest tests/integration/

# Run linting checks
lint: $(VENV_NAME)
	$(VENV_BIN)/flake8 src/ tests/
	$(VENV_BIN)/mypy src/ --exclude alembic/
	$(VENV_BIN)/black --check src/ tests/

# Format code
format: $(VENV_NAME)
	$(VENV_BIN)/black src/ tests/

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/
	rm -rf $(VENV_NAME)/

# Build Docker image
build:
	docker build -t product-management-api .

# Run application locally
run: $(VENV_NAME)
	$(VENV_BIN)/uvicorn src.presentation.main:app --reload --host 0.0.0.0 --port 8000

# Docker commands
docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Database migration commands
migrate: $(VENV_NAME)
	$(VENV_BIN)/alembic upgrade head

migrate-up: $(VENV_NAME)
	$(VENV_BIN)/alembic upgrade head

migrate-down: $(VENV_NAME)
	$(VENV_BIN)/alembic downgrade -1

migrate-status: $(VENV_NAME)
	@echo "📊 Current migration status:"
	@$(VENV_BIN)/alembic current
	@echo ""
	@echo "📋 Migration history:"
	@$(VENV_BIN)/alembic history --verbose

migrate-to: $(VENV_NAME)
	@if [ -z "$(REV)" ]; then \
		echo "❌ Please specify revision: make migrate-to REV=<revision>"; \
		echo "💡 Use 'make migrate-status' to see available revisions"; \
		exit 1; \
	fi
	@echo "🔄 Migrating to revision: $(REV)"
	$(VENV_BIN)/alembic upgrade $(REV)

create-migration: $(VENV_NAME)
	@echo "📝 Creating new migration..."
	@read -p "Enter migration name: " name; \
	if [ -z "$$name" ]; then \
		echo "❌ Migration name cannot be empty"; \
		exit 1; \
	fi; \
	LAST_REV=$$($(VENV_BIN)/alembic heads 2>/dev/null | head -1 | cut -d' ' -f1 2>/dev/null || echo "000"); \
	if [ "$$LAST_REV" = "000" ]; then \
		NEXT_REV="001"; \
	else \
		LAST_NUM=$$(echo "$$LAST_REV" | sed 's/^0*//'); \
		if [ -z "$$LAST_NUM" ]; then LAST_NUM=0; fi; \
		NEXT_NUM=$$(($$LAST_NUM + 1)); \
		NEXT_REV=$$(printf "%03d" $$NEXT_NUM); \
	fi; \
	echo "🔢 Next revision will be: $$NEXT_REV"; \
	$(VENV_BIN)/alembic revision --autogenerate -m "$$name" --rev-id "$$NEXT_REV"
	@echo "✅ Migration created successfully"

# Development setup
dev-setup: install
	cp env.example .env
	@echo "Development environment setup complete!"
	@echo "Virtual environment created at: $(VENV_NAME)"
	@echo "Please edit .env file with your configuration."
	@echo "To activate the virtual environment, run: source $(VENV_BIN)/activate"

# Full development workflow
dev: dev-setup docker-build docker-run
	@echo "Development environment is ready!"
	@echo "API is available at: http://localhost:8000"
	@echo "Swagger UI: http://localhost:8000/docs"
	@echo "ReDoc: http://localhost:8000/redoc"

# Production build
prod-build:
	docker-compose -f docker-compose.prod.yml build

# Production run
prod-run:
	docker-compose -f docker-compose.prod.yml up -d

# Production stop
prod-stop:
	docker-compose -f docker-compose.prod.yml down 