# Script para configurar el entorno de desarrollo en Windows

Write-Host "🚀 Configurando entorno de desarrollo..." -ForegroundColor Green

# Verificar Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python no está instalado" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python encontrado" -ForegroundColor Green

# Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker no está instalado" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker encontrado" -ForegroundColor Green

# Verificar Docker Compose
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose no está instalado" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker Compose encontrado" -ForegroundColor Green

# Instalar dependencias de desarrollo
Write-Host "📦 Instalando dependencias de desarrollo..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install black isort flake8 pylint pytest pytest-cov pytest-asyncio bandit pre-commit

# Configurar pre-commit
Write-Host "🔧 Configurando pre-commit hooks..." -ForegroundColor Cyan
pre-commit install

# Crear archivo .env si no existe
if (-not (Test-Path .env)) {
    Write-Host "📝 Creando archivo .env..." -ForegroundColor Cyan
    @"
MONGO_ROOT_USER=root
MONGO_ROOT_PASSWORD=example
JWT_SECRET=your-secret-key-change-this-in-production
"@ | Out-File -FilePath .env -Encoding UTF8
    Write-Host "⚠️  Recuerda actualizar las variables en .env" -ForegroundColor Yellow
}

# Levantar servicios
Write-Host "🐳 Levantando servicios Docker..." -ForegroundColor Cyan
docker-compose up -d mongodb

Write-Host "⏳ Esperando que MongoDB esté listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "✅ Entorno de desarrollo configurado!" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos útiles:" -ForegroundColor Cyan
Write-Host "  python -m pytest           - Ejecutar tests"
Write-Host "  black .                    - Formatear código"
Write-Host "  docker-compose up          - Levantar servicios"
Write-Host ""
Write-Host "API Gateway: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "MongoDB: mongodb://root:example@localhost:27017" -ForegroundColor Yellow
