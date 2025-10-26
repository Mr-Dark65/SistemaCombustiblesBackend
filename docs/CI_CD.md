# CI/CD Pipeline Documentation

## Resumen

Este proyecto implementa un pipeline completo de CI/CD utilizando GitHub Actions para automatizar el proceso de integración continua y despliegue continuo.

## Estructura de Workflows

### 1. CI Pipeline (`ci.yml`)

Se ejecuta en cada push y pull request a las ramas principales.

**Jobs incluidos:**
- **Lint & Code Quality**: Verifica el formato y calidad del código
  - Black (formateo)
  - isort (ordenamiento de imports)
  - Flake8 (linting)
  - Pylint (análisis estático)
  - Bandit (seguridad)
  
- **Unit Tests**: Ejecuta tests unitarios para cada servicio
  - Tests paralelos por servicio
  - Cobertura de código con pytest-cov
  - Upload a Codecov
  
- **SonarQube Analysis**: Análisis de calidad de código
  - Quality Gate check
  - Code smells, bugs, vulnerabilities
  
- **Build Docker Images**: Construye imágenes Docker
  - Build paralelo de todos los servicios
  - Push a Docker Hub (solo en push a main)
  - Versionado automático con tags
  
- **Security Scan**: Escaneo de seguridad
  - Trivy para vulnerabilidades
  - Upload a GitHub Security
  
- **Integration Tests**: Tests de integración
  - MongoDB como servicio
  - Tests end-to-end

### 2. CD Pipeline (`cd.yml`)

Se ejecuta en push a main o tags de versión.

**Environments:**
- **Staging**: Deploy automático desde main
- **Production**: Deploy desde tags (v*)

**Jobs incluidos:**
- Deploy to Staging
- Deploy to Production
- Create GitHub Release
- Notificaciones

### 3. PR Checks (`pr-checks.yml`)

Validaciones específicas para Pull Requests.

**Incluye:**
- Validación de título de PR (Conventional Commits)
- Detección de cambios por servicio
- Code review automatizado
- Dependency review
- Check de tamaño de PR

## Configuración Requerida

### GitHub Secrets

Debes configurar los siguientes secrets en tu repositorio de GitHub:

#### Docker Hub
```
DOCKER_USERNAME: tu_usuario_dockerhub
DOCKER_PASSWORD: tu_password_dockerhub
```

#### SonarQube
```
SONAR_TOKEN: tu_token_sonarqube
SONAR_HOST_URL: http://tu-sonarqube-server:9000
```

#### Aplicación
```
MONGO_ROOT_USER: usuario_mongodb
MONGO_ROOT_PASSWORD: password_mongodb
JWT_SECRET: tu_secreto_jwt
```

#### Deploy (Producción)
```
SSH_PRIVATE_KEY: tu_clave_ssh_privada
PRODUCTION_HOST: ip_o_dominio_servidor
PRODUCTION_USER: usuario_servidor
PRODUCTION_URL: https://tu-dominio.com
```

### Configurar Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Click en "New repository secret"
4. Añade cada secret con su valor

## Uso

### Para desarrolladores

#### 1. Crear una nueva feature
```bash
git checkout -b feature/nueva-funcionalidad
# Hacer cambios...
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

#### 2. Crear Pull Request
- El PR debe tener un título siguiendo Conventional Commits
- Ejemplos: `feat:`, `fix:`, `docs:`, `refactor:`, etc.
- Los checks automáticos se ejecutarán

#### 3. Merge a develop/main
- Después del merge, se ejecuta el CI completo
- Si es a main, también se despliega a staging

#### 4. Release a Producción
```bash
git tag v1.0.0
git push origin v1.0.0
```
- Esto dispara el deploy a producción
- Se crea un release en GitHub automáticamente

## Herramientas de Calidad

### Black
Formateo automático de código Python.
```bash
black .
```

### isort
Ordenamiento de imports.
```bash
isort .
```

### Flake8
Linting de código.
```bash
flake8 .
```

### Pytest
Ejecución de tests.
```bash
pytest tests/ -v --cov=.
```

### Bandit
Análisis de seguridad.
```bash
bandit -r . -f json -o bandit-report.json
```

## Convenciones de Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato
- `refactor:` Refactorización de código
- `perf:` Mejoras de rendimiento
- `test:` Añadir o modificar tests
- `build:` Cambios en build o dependencias
- `ci:` Cambios en CI/CD
- `chore:` Tareas de mantenimiento

## Monitoreo

### Ver estado de pipelines
1. Ve a la pestaña "Actions" en GitHub
2. Selecciona el workflow que quieres ver
3. Revisa los logs de cada job

### Codecov
- Los reportes de cobertura se suben automáticamente
- Configura Codecov en: https://codecov.io/

### SonarQube
- Accede a tu instancia de SonarQube
- Revisa métricas de calidad, bugs, vulnerabilidades

## Troubleshooting

### El build falla en tests
1. Ejecuta los tests localmente: `pytest tests/ -v`
2. Corrige los errores
3. Commit y push de nuevo

### El build falla en linting
1. Ejecuta las herramientas localmente:
   ```bash
   black --check .
   flake8 .
   isort --check-only .
   ```
2. Aplica correcciones automáticas:
   ```bash
   black .
   isort .
   ```

### El deploy falla
1. Revisa los logs en GitHub Actions
2. Verifica que los secrets estén configurados
3. Verifica la conectividad SSH (para producción)

### Docker build falla
1. Prueba el build localmente:
   ```bash
   docker build -t test ./auth-service
   ```
2. Revisa el Dockerfile y dependencias

## Mejores Prácticas

1. **Escribe tests**: Cada nueva feature debe incluir tests
2. **Mantén alta cobertura**: Apunta a >80% de cobertura
3. **Commits pequeños**: Haz commits frecuentes y pequeños
4. **PRs revisables**: Mantén los PRs < 500 líneas
5. **Documenta cambios**: Actualiza README y documentación
6. **Revisa SonarQube**: No ignores los code smells
7. **Prueba localmente**: Ejecuta tests y linters antes de push

## Referencias

- [GitHub Actions](https://docs.github.com/en/actions)
- [Docker](https://docs.docker.com/)
- [SonarQube](https://docs.sonarqube.org/)
- [Pytest](https://docs.pytest.org/)
- [Black](https://black.readthedocs.io/)
