# Makefile para comandos comunes del proyecto

.PHONY: help install test lint format clean docker-build docker-up docker-down proto

# Variables
PYTHON := python
PIP := pip
DOCKER_COMPOSE := docker-compose

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias de desarrollo
	$(PIP) install black isort flake8 pylint pytest pytest-cov pytest-asyncio bandit pre-commit
	pre-commit install

install-service: ## Instalar dependencias de un servicio específico (uso: make install-service SERVICE=auth-service)
	$(PIP) install -r $(SERVICE)/requirements.txt

test: ## Ejecutar todos los tests
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

test-unit: ## Ejecutar solo tests unitarios
	pytest -m "not integration" -v

test-integration: ## Ejecutar solo tests de integración
	pytest -m integration -v

test-service: ## Ejecutar tests de un servicio (uso: make test-service SERVICE=auth-service)
	cd $(SERVICE) && pytest tests/ -v --cov=. --cov-report=term

lint: ## Ejecutar linters
	black --check .
	isort --check-only .
	flake8 .
	pylint **/*.py --exclude-patterns="*_pb2*.py" || true

format: ## Formatear código automáticamente
	black .
	isort .

security: ## Análisis de seguridad
	bandit -r . -f json -o bandit-report.json
	@echo "Reporte generado en bandit-report.json"

clean: ## Limpiar archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage coverage.xml bandit-report.json

docker-build: ## Construir todas las imágenes Docker
	$(DOCKER_COMPOSE) build

docker-up: ## Levantar todos los servicios
	$(DOCKER_COMPOSE) up -d

docker-down: ## Detener todos los servicios
	$(DOCKER_COMPOSE) down

docker-logs: ## Ver logs de todos los servicios
	$(DOCKER_COMPOSE) logs -f

docker-clean: ## Limpiar contenedores y volúmenes
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

proto-auth: ## Regenerar código de auth.proto
	cd auth-service && $(PYTHON) -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/auth.proto

proto-vehicle: ## Regenerar código de vehicles.proto
	cd vehicle-service && $(PYTHON) -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/vehicles.proto

proto-route: ## Regenerar código de routes.proto
	cd route-service && $(PYTHON) -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/routes.proto

proto-fuel: ## Regenerar código de fuel.proto
	cd fuel-consumption-service && $(PYTHON) -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/fuel.proto

proto-driver: ## Regenerar código de drivers.proto
	cd driver-service && $(PYTHON) -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/drivers.proto

proto-all: ## Regenerar todos los archivos proto
	$(MAKE) proto-auth
	$(MAKE) proto-vehicle
	$(MAKE) proto-route
	$(MAKE) proto-fuel
	$(MAKE) proto-driver

dev-auth: ## Ejecutar auth-service en modo desarrollo
	cd auth-service && $(PYTHON) server/server.py

dev-vehicle: ## Ejecutar vehicle-service en modo desarrollo
	cd vehicle-service && $(PYTHON) server/server.py

dev-route: ## Ejecutar route-service en modo desarrollo
	cd route-service && $(PYTHON) server/server.py

dev-fuel: ## Ejecutar fuel-consumption-service en modo desarrollo
	cd fuel-consumption-service && $(PYTHON) server/server.py

dev-driver: ## Ejecutar driver-service en modo desarrollo
	cd driver-service && $(PYTHON) server/server.py

dev-gateway: ## Ejecutar api-gateway en modo desarrollo
	cd api-gateway && uvicorn main:app --reload

sonar: ## Ejecutar análisis de SonarQube
	sonar-scanner

pre-commit: ## Ejecutar pre-commit en todos los archivos
	pre-commit run --all-files

check: lint test ## Ejecutar todos los checks (lint + tests)

ci-local: clean lint test ## Simular pipeline CI localmente

setup-dev: install docker-up ## Configuración completa para desarrollo
	@echo "Entorno de desarrollo configurado!"
	@echo "API Gateway disponible en: http://localhost:8000/docs"
