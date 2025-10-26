#!/bin/bash

# Script para configurar el entorno de desarrollo

echo "🚀 Configurando entorno de desarrollo..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

echo "✅ Python 3 encontrado"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

echo "✅ Docker encontrado"

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

echo "✅ Docker Compose encontrado"

# Instalar dependencias de desarrollo
echo "📦 Instalando dependencias de desarrollo..."
pip install --upgrade pip
pip install black isort flake8 pylint pytest pytest-cov pytest-asyncio bandit pre-commit

# Configurar pre-commit
echo "🔧 Configurando pre-commit hooks..."
pre-commit install

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cat > .env << EOF
MONGO_ROOT_USER=root
MONGO_ROOT_PASSWORD=example
JWT_SECRET=your-secret-key-change-this-in-production
EOF
    echo "⚠️  Recuerda actualizar las variables en .env"
fi

# Levantar servicios
echo "🐳 Levantando servicios Docker..."
docker-compose up -d mongodb

echo "⏳ Esperando que MongoDB esté listo..."
sleep 10

echo ""
echo "✅ Entorno de desarrollo configurado!"
echo ""
echo "Comandos útiles:"
echo "  make help              - Ver todos los comandos disponibles"
echo "  make docker-up         - Levantar todos los servicios"
echo "  make test              - Ejecutar tests"
echo "  make lint              - Ejecutar linters"
echo "  make format            - Formatear código"
echo ""
echo "API Gateway: http://localhost:8000/docs"
echo "MongoDB: mongodb://root:example@localhost:27017"
