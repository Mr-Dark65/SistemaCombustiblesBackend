# Backend Microservicios - Gestión de Vehículos, Rutas, Consumo y Choferes

[![CI Pipeline](https://github.com/Mr-Dark65/SistemaCombustiblesBackend/workflows/CI%20Pipeline/badge.svg)](https://github.com/Mr-Dark65/SistemaCombustiblesBackend/actions)
[![CD Pipeline](https://github.com/Mr-Dark65/SistemaCombustiblesBackend/workflows/CD%20Pipeline/badge.svg)](https://github.com/Mr-Dark65/SistemaCombustiblesBackend/actions)
[![codecov](https://codecov.io/gh/Mr-Dark65/SistemaCombustiblesBackend/branch/main/graph/badge.svg)](https://codecov.io/gh/Mr-Dark65/SistemaCombustiblesBackend)

Este proyecto implementa un sistema de gestión de flotas basado en microservicios, utilizando Python, gRPC, FastAPI y MongoDB, orquestado con Docker Compose. Incluye autenticación, gestión de vehículos, rutas, consumo de combustible y choferes, todo accesible de forma segura a través de un API Gateway.

**✨ Características destacadas:**
- 🚀 CI/CD automatizado con GitHub Actions
- 🧪 Tests automatizados y cobertura de código
- 🔒 Análisis de seguridad integrado
- 📊 Monitoreo de calidad con SonarQube
- 🐳 Despliegue con Docker y Docker Compose
- 📨 Mensajería asíncrona con Apache Kafka

## Arquitectura

- **API Gateway**: Expone una API REST (FastAPI) que unifica y protege el acceso a los microservicios, validando tokens y roles.
- **auth-service**: Servicio de autenticación y autorización (gRPC, JWT, MongoDB).
- **vehicle-service**: Gestión de vehículos y asignación de choferes (gRPC, MongoDB).
- **route-service**: Gestión de rutas y asociación con vehículos (gRPC, MongoDB).
- **fuel-consumption-service**: Registro y consulta de consumos de combustible, reportes y comparaciones (gRPC, MongoDB).
- **driver-service**: Registro, consulta, actualización y asignación de choferes (gRPC, MongoDB).
- **MongoDB**: Base de datos centralizada para todos los servicios.

## Tecnologías principales

- Python 3.9+
- FastAPI (API Gateway)
- gRPC (comunicación entre servicios)
- MongoDB (persistencia)
- Docker & Docker Compose (orquestación)
- Protobuf (definición de contratos)
- JWT (autenticación)

## Estructura del repositorio

```
Backend/
  ├── api-gateway/
  ├── auth-service/
  ├── vehicle-service/
  ├── route-service/
  ├── fuel-consumption-service/
  ├── driver-service/
  └── docker-compose.yml
```

## 🚀 Inicio Rápido

### Opción 1: Script de configuración automática

**Windows:**
```powershell
.\scripts\setup-dev.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh
```

### Opción 2: Configuración manual

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Mr-Dark65/SistemaCombustiblesBackend.git
   cd SistemaCombustiblesBackend
   ```

2. **Configura variables de entorno:**
   ```bash
   # Crea archivo .env
   cp .env.example .env
   # Edita .env con tus valores
   ```

3. **Levanta todos los servicios:**
   ```bash
   docker-compose up --build
   ```

4. **Accede a la aplicación:**
   - 📖 API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - 🗄️ MongoDB: `mongodb://root:example@localhost:27017`

### Opción 3: Usando Makefile

```bash
# Ver todos los comandos disponibles
make help

# Configurar entorno completo
make setup-dev

# Ejecutar tests
make test

# Formatear código
make format
```

## Servicios y puertos

| Servicio                   | Puerto | Descripción                                 |
|----------------------------|--------|---------------------------------------------|
| MongoDB                    | 27017  | Base de datos                               |
| auth-service               | 50051  | Autenticación y JWT                         |
| vehicle-service            | 50052  | Gestión de vehículos                        |
| route-service              | 50053  | Gestión de rutas                            |
| fuel-consumption-service   | 50054  | Consumo de combustible                      |
| driver-service             | 50055  | Gestión de choferes                         |
| api-gateway                | 8000   | API REST unificada                          |

## Endpoints principales

- **Autenticación:** `/register`, `/login`, `/validate-token`
- **Vehículos:** `/vehicles`, `/vehicles/{id}`, `/vehicles/{id}/status`, `/vehicles/{id}/assign-driver`
- **Rutas:** `/routes`, `/routes/{id}`, `/routes/{id}/assign-vehicle`, `/routes/{id}/fuel-consumption`
- **Consumo de combustible:** `/fuel`, `/fuel/{id}`, `/fuel/report/by-vehicle-type`, `/fuel/compare/{route_id}`
- **Choferes:** `/drivers`, `/drivers/{id}`, `/drivers/{id}/assign`

> Todos los endpoints (excepto login y register) requieren autenticación mediante token JWT.

## 🛠️ Desarrollo

### Configuración del entorno de desarrollo

Ver la [Guía de Desarrollo](docs/DEVELOPMENT.md) completa.

```bash
# Instalar dependencias de desarrollo
pip install black isort flake8 pylint pytest pytest-cov

# Configurar pre-commit hooks
pre-commit install

# Ejecutar tests
pytest tests/ -v

# Formatear código
black .
isort .

# Linting
flake8 .
```

### Modificar contratos gRPC

```bash
# Regenerar un servicio específico
make proto-auth

# Regenerar todos
make proto-all
```

### Comandos útiles

```bash
make test              # Ejecutar todos los tests
make lint              # Verificar calidad de código
make format            # Formatear código automáticamente
make docker-up         # Levantar servicios
make docker-down       # Detener servicios
make clean             # Limpiar archivos temporales
```

## 🔒 Seguridad y Control de Acceso

- **Autenticación JWT**: Todos los endpoints requieren token válido
- **Roles y permisos**: `Admin`, `Operador`, `Supervisor`
- **Análisis de seguridad**: Bandit y Trivy en CI/CD
- **Variables seguras**: Uso de GitHub Secrets

## 🧪 Testing

### Estructura de tests

```
tests/
├── integration/         # Tests de integración E2E
│   └── test_e2e.py
auth-service/tests/     # Tests del servicio de auth
vehicle-service/tests/  # Tests del servicio de vehículos
...
```

### Ejecutar tests

```bash
# Todos los tests
pytest

# Solo tests unitarios
pytest -m "not integration"

# Solo tests de integración
pytest -m integration

# Con cobertura
pytest --cov=. --cov-report=html
```

## 📊 CI/CD

Este proyecto implementa un pipeline completo de CI/CD. Ver [Documentación de CI/CD](docs/CI_CD.md).

### Workflows de GitHub Actions

- **CI Pipeline** (`.github/workflows/ci.yml`): Se ejecuta en cada push/PR
  - Linting y formateo
  - Tests unitarios
  - Análisis con SonarQube
  - Build de imágenes Docker
  - Escaneo de seguridad
  - Tests de integración

- **CD Pipeline** (`.github/workflows/cd.yml`): Deploy automático
  - Staging: Push a `main`
  - Production: Tags `v*`

- **PR Checks** (`.github/workflows/pr-checks.yml`): Validaciones de PRs

### Configuración de Secrets

Ver [Guía de Configuración de Secrets](docs/SECRETS_SETUP.md).

Secrets necesarios:
- `DOCKER_USERNAME`, `DOCKER_PASSWORD`
- `SONAR_TOKEN`, `SONAR_HOST_URL`
- `MONGO_ROOT_USER`, `MONGO_ROOT_PASSWORD`, `JWT_SECRET`

### Pipeline local

```bash
# Ejecutar CI localmente
./scripts/ci-local.sh

# Ejecutar todos los tests
./scripts/run-all-tests.sh
```

## 📈 Monitoreo y Calidad

- **Cobertura de código**: Codecov
- **Calidad de código**: SonarQube
- **Seguridad**: Bandit, Trivy
- **Logging**: Logs centralizados en cada servicio

## 📝 Logging

Todos los microservicios implementan logging estructurado:

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f auth-service
```

## 🚀 Despliegue

### Staging
Push a `main` → Deploy automático a staging

### Production
```bash
git tag v1.0.0
git push origin v1.0.0
```
→ Deploy automático a producción + GitHub Release

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "feat: agregar nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

### Convenciones de commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `test:` Tests
- `refactor:` Refactorización
- `ci:` Cambios en CI/CD

## 📚 Documentación Adicional

- [Guía de Desarrollo](docs/DEVELOPMENT.md)
- [Documentación de CI/CD](docs/CI_CD.md)
- [Configuración de Secrets](docs/SECRETS_SETUP.md)
- [README de cada servicio](./auth-service/README.md)

## 🔧 Troubleshooting

Ver sección de Troubleshooting en la [Guía de Desarrollo](docs/DEVELOPMENT.md#troubleshooting-común).

## Integración de Kafka y mensajería entre microservicios

El sistema utiliza Apache Kafka como bus de eventos para la comunicación asíncrona entre microservicios. Esto permite desacoplar los servicios y facilitar la auditoría, la integración y la escalabilidad.

### Servicios involucrados y topics

- **vehicle-service**: Publica eventos en el topic `vehicle-events` (creación, actualización de estado, asignación de chofer).
- **route-service**: Publica eventos en `route-events` (creación, actualización, asignación de vehículo) y consume de `vehicle-events`.
- **driver-service**: Publica eventos en `driver-events` (registro, actualización, asignación).
- **fuel-consumption-service**: Publica eventos en `fuel-consumption-events` (registro de consumo) y consume de `vehicle-events` y `route-events`.
- **auth-service**: Publica eventos de auditoría en `auth-events` (registro, login, login fallido) y puede consumirlos para auditoría.

### Ejemplo de evento publicado
```json
{
  "type": "CREATED",
  "entity": "vehicle",
  "data": {
    "id": "...",
    "plate": "ABC123",
    "type": "Liviana",
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2020,
    "status": "Disponible"
  }
}
```

### Cómo ver los mensajes de Kafka

1. **Desde la consola del contenedor Kafka:**
   ```sh
   docker exec -it xyz-kafka bash
   kafka-console-consumer --bootstrap-server localhost:9092 --topic vehicle-events --from-beginning
   ```
   Cambia `vehicle-events` por el topic que quieras ver.

2. **Con herramientas visuales:**
   Puedes agregar Kafdrop o Kafka UI a tu `docker-compose.yml` para monitorear topics y mensajes desde el navegador.

### Variables de entorno relevantes

- `KAFKA_BROKER`: Dirección del broker Kafka (por defecto `kafka:9092` en Docker Compose).
- `VEHICLE_TOPIC`, `ROUTE_TOPIC`, `DRIVER_TOPIC`, `FUEL_TOPIC`, `AUTH_TOPIC`: Permiten personalizar los nombres de los topics si lo deseas.

### Notas
- Todos los microservicios publican eventos relevantes en Kafka automáticamente.
- Puedes consumir estos eventos desde otros servicios o herramientas para auditoría, integración o análisis en tiempo real. 