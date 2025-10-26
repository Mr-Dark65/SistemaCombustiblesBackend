# 🚀 Guía Rápida de 5 Minutos

## ¿Qué se ha implementado?

Un **pipeline completo de CI/CD** con GitHub Actions que incluye:
- ✅ Tests automatizados
- ✅ Análisis de calidad (SonarQube)
- ✅ Análisis de seguridad (Bandit, Trivy)
- ✅ Build de Docker images
- ✅ Deploy automático

## 🎯 Pasos para Activar (AHORA)

### 1️⃣ Configurar GitHub Secrets (2 minutos)

Ve a: **GitHub → Settings → Secrets and variables → Actions**

```yaml
# Mínimos necesarios:
DOCKER_USERNAME: tu_usuario_dockerhub
DOCKER_PASSWORD: tu_password_dockerhub
SONAR_TOKEN: tu_token_sonarqube  
SONAR_HOST_URL: http://localhost:9000
MONGO_ROOT_USER: root
MONGO_ROOT_PASSWORD: example
JWT_SECRET: genera_uno_aleatorio_largo
```

**Generar JWT_SECRET:**
```powershell
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

### 2️⃣ Habilitar GitHub Actions (30 segundos)

**GitHub → Settings → Actions → General**
- ✅ Allow all actions and reusable workflows
- ✅ Read and write permissions

### 3️⃣ Setup Local (1 minuto)

```powershell
# Windows PowerShell
.\scripts\setup-dev.ps1

# Crear .env
Copy-Item .env.example .env
# Editar .env con tus valores
```

### 4️⃣ Primer Push (30 segundos)

```powershell
git add .
git commit -m "ci: add complete CI/CD pipeline"
git push
```

### 5️⃣ Verificar (1 minuto)

1. Ve a GitHub → Pestaña **Actions**
2. Verás el workflow ejecutándose
3. ¡Espera a que termine! ⏱️

## 🎨 Estructura Visual del Pipeline

```
PUSH/PR
   │
   ├─► LINT (2 min)
   │   ├─ Black ✓
   │   ├─ isort ✓
   │   ├─ Flake8 ✓
   │   └─ Pylint ✓
   │
   ├─► TESTS (5 min)
   │   ├─ auth-service ✓
   │   ├─ vehicle-service ✓
   │   ├─ route-service ✓
   │   ├─ fuel-service ✓
   │   ├─ driver-service ✓
   │   └─ api-gateway ✓
   │
   ├─► SONARQUBE (3 min)
   │   └─ Quality Gate ✓
   │
   ├─► BUILD DOCKER (10 min)
   │   └─ Push to Hub ✓
   │
   ├─► SECURITY (5 min)
   │   ├─ Bandit ✓
   │   └─ Trivy ✓
   │
   └─► INTEGRATION (3 min)
       └─ E2E Tests ✓

Total: ~25-30 min
```

## 📦 Archivos Importantes

```
SistemaCombustiblesBackend/
│
├── .github/workflows/      ← 🎯 Workflows de CI/CD
│   ├── ci.yml             ← Pipeline principal
│   ├── cd.yml             ← Deploy automático
│   └── pr-checks.yml      ← Validaciones de PR
│
├── docs/                   ← 📚 Documentación
│   ├── CI_CD.md           ← Lee esto primero
│   ├── SECRETS_SETUP.md   ← Configurar secrets
│   └── DEVELOPMENT.md     ← Guía de desarrollo
│
├── scripts/                ← 🔧 Scripts útiles
│   ├── setup-dev.ps1      ← Ejecuta este
│   └── ci-local.sh        ← CI en local
│
├── CHECKLIST.md           ← ✅ Lista completa
├── .env.example           ← Template de .env
└── Makefile              ← Comandos útiles
```

## 🛠️ Comandos Esenciales

```powershell
# Ver todos los comandos disponibles
make help

# Formatear código (antes de commit)
black .
isort .

# Verificar código (antes de push)
flake8 .

# Ejecutar tests
pytest tests/ -v

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🎓 Workflow de Desarrollo

```
1. Crear rama
   git checkout -b feature/mi-feature

2. Hacer cambios
   code .
   
3. Formatear
   black .
   isort .

4. Tests
   pytest tests/ -v

5. Commit
   git add .
   git commit -m "feat: mi cambio"

6. Push
   git push origin feature/mi-feature

7. Crear PR
   GitHub → New Pull Request

8. Esperar CI ✅

9. Merge
   Squash and merge
```

## 🔥 Tips Rápidos

### Pre-commit (Recomendado)
```powershell
pip install pre-commit
pre-commit install
# Ahora se ejecuta automáticamente en cada commit
```

### Ver coverage
```powershell
pytest --cov=. --cov-report=html
# Abre: htmlcov/index.html
```

### CI Local (antes de push)
```bash
./scripts/ci-local.sh
# Ejecuta todo el pipeline localmente
```

### Docker limpio
```powershell
docker-compose down -v
docker system prune -f
docker-compose up --build
```

## ⚡ Solución Rápida de Problemas

### Error: "Secret not found"
→ Configura los secrets en GitHub (Paso 1)

### Error: "Black would reformat"
→ Ejecuta: `black .`

### Error: "Imports are not sorted"
→ Ejecuta: `isort .`

### Tests fallan
→ Los tests son templates, necesitas implementarlos

### Docker build falla
→ Verifica Dockerfile y requirements.txt

### No puedo hacer push
→ Instala Git LFS si tienes archivos grandes

## 📊 Después del Primer Push

Verás en GitHub:
1. ✅ Badge de build en README
2. 📊 Resultados de tests
3. 🔒 Reporte de seguridad
4. 📈 Cobertura (si configuras Codecov)
5. 🎯 Métricas de SonarQube

## 🎯 Checklist Mínimo

Antes de tu primer push, asegúrate:
- [ ] Secrets configurados en GitHub
- [ ] GitHub Actions habilitado
- [ ] Archivo .env creado localmente
- [ ] `black .` ejecutado
- [ ] `isort .` ejecutado

## 🚀 Deploy

### A Staging (automático)
```powershell
git checkout main
git merge feature/mi-feature
git push
# Deploy automático a staging
```

### A Production (con tag)
```powershell
git tag v1.0.0
git push origin v1.0.0
# Deploy automático a producción
```

## 📞 Necesitas Más Info?

1. **Detalles completos**: `docs/CI_CD.md`
2. **Lista paso a paso**: `CHECKLIST.md`
3. **Desarrollo**: `docs/DEVELOPMENT.md`
4. **Secrets**: `docs/SECRETS_SETUP.md`

## 🎉 ¡Listo!

Con estos 5 pasos tienes CI/CD funcionando.

**Siguiente**: Abre `CHECKLIST.md` para la guía completa.

---

**Tiempo total**: 5 minutos ⏱️  
**Resultado**: Pipeline profesional de CI/CD 🚀
