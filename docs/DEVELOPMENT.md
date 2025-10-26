# Guía de Desarrollo

## Configuración del Entorno de Desarrollo

### Prerrequisitos
- Python 3.11+
- Docker y Docker Compose
- Git
- VS Code (recomendado)

### Configuración Inicial

1. **Clonar el repositorio**
   ```bash
   git clone <repo-url>
   cd SistemaCombustiblesBackend
   ```

2. **Configurar entorno virtual (opcional para desarrollo local)**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias de desarrollo**
   ```bash
   pip install black isort flake8 pylint pytest pytest-cov pytest-asyncio bandit
   ```

4. **Configurar pre-commit hooks (opcional)**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Estructura de Desarrollo

### Workflow de Git

1. **Crear rama de feature**
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```

2. **Hacer cambios y commits**
   ```bash
   git add .
   git commit -m "feat: descripción del cambio"
   ```

3. **Mantener actualizado con main**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **Push y crear PR**
   ```bash
   git push origin feature/nombre-descriptivo
   ```

### Desarrollo Local

#### Levantar servicios con Docker Compose
```bash
docker-compose up --build
```

#### Levantar servicios individuales
```bash
# Solo MongoDB
docker-compose up mongodb

# Solo un servicio específico
docker-compose up auth-service
```

#### Desarrollo sin Docker (servicio individual)
```bash
cd auth-service
pip install -r requirements.txt
python server/server.py
```

## Escribir Tests

### Tests Unitarios

Ubicación: `<servicio>/tests/test_*.py`

```python
import pytest
from unittest.mock import Mock, patch

def test_ejemplo():
    # Arrange
    dato = "test"
    
    # Act
    resultado = funcion_a_probar(dato)
    
    # Assert
    assert resultado == "esperado"
```

### Tests de Integración

Ubicación: `tests/integration/test_*.py`

```python
import pytest

@pytest.mark.integration
def test_integracion_ejemplo():
    # Test que requiere servicios externos
    pass
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests de un servicio específico
pytest auth-service/tests/

# Solo tests unitarios
pytest -m "not integration"

# Solo tests de integración
pytest -m integration

# Con cobertura
pytest --cov=. --cov-report=html
```

## Calidad de Código

### Formateo Automático

```bash
# Formatear con Black
black .

# Ordenar imports con isort
isort .
```

### Linting

```bash
# Flake8
flake8 .

# Pylint
pylint **/*.py --exclude-patterns="*_pb2*.py"
```

### Análisis de Seguridad

```bash
# Bandit
bandit -r . -f json -o report.json
```

### Pre-commit (automático)

Crea `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Modificar Protobuf

### Editar archivo .proto

```bash
cd <servicio>/protos
# Editar el archivo .proto
```

### Regenerar código Python

```bash
python -m grpc_tools.protoc \
  -I=protos \
  --python_out=server \
  --grpc_python_out=server \
  protos/nombre.proto
```

## Debugging

### Debugging en VS Code

Crear `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Auth Service",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/auth-service/server/server.py",
      "console": "integratedTerminal",
      "env": {
        "DB_HOST": "localhost",
        "JWT_SECRET": "test-secret"
      }
    }
  ]
}
```

### Logs

Ver logs de servicios:
```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f auth-service
```

## Base de Datos

### Conectar a MongoDB

```bash
# Desde contenedor
docker exec -it xyz-mongodb mongosh -u root -p example

# Desde local
mongosh mongodb://root:example@localhost:27017
```

### Ver colecciones

```javascript
use auth_service
show collections
db.users.find()
```

## Variables de Entorno

### Archivo .env (no versionado)

```env
MONGO_ROOT_USER=root
MONGO_ROOT_PASSWORD=example
JWT_SECRET=your-secret-key-here
```

### Usar en código

```python
import os
from dotenv import load_dotenv

load_dotenv()

jwt_secret = os.getenv('JWT_SECRET')
```

## Troubleshooting Común

### Puerto ya en uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Limpiar Docker
```bash
docker-compose down -v
docker system prune -a
```

### Regenerar dependencias
```bash
pip freeze > requirements.txt
```

### MongoDB no inicia
```bash
docker-compose down
docker volume rm sistemacombustiblesbackend_mongodb_data
docker-compose up mongodb
```

## Mejores Prácticas

1. **Siempre usar type hints**
   ```python
   def funcion(param: str) -> dict:
       return {"result": param}
   ```

2. **Documentar funciones**
   ```python
   def funcion(param: str) -> dict:
       """
       Descripción de la función.
       
       Args:
           param: Descripción del parámetro
           
       Returns:
           Descripción del retorno
       """
       return {"result": param}
   ```

3. **Manejo de errores**
   ```python
   try:
       resultado = operacion_riesgosa()
   except SpecificException as e:
       logger.error(f"Error: {e}")
       raise
   ```

4. **Logging apropiado**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   logger.info("Mensaje informativo")
   logger.error("Error ocurrido", exc_info=True)
   ```

5. **Tests para cada nueva feature**
   - Mínimo 80% de cobertura
   - Tests unitarios + integración
   - Mock de dependencias externas

## Recursos

- [Python Best Practices](https://docs.python-guide.org/)
- [gRPC Python Docs](https://grpc.io/docs/languages/python/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Pytest Docs](https://docs.pytest.org/)
