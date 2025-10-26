#!/bin/bash

# Script para ejecutar el pipeline CI localmente

echo "🔍 Ejecutando pipeline CI localmente..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir errores
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Función para imprimir éxitos
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Función para imprimir advertencias
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Paso 1: Limpiar archivos temporales
echo ""
echo "🧹 Limpiando archivos temporales..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
success "Limpieza completada"

# Paso 2: Black (formateo)
echo ""
echo "🎨 Verificando formateo con Black..."
if black --check --diff . ; then
    success "Formateo correcto"
else
    error "Errores de formateo encontrados"
    warning "Ejecuta 'black .' para corregir"
    exit 1
fi

# Paso 3: isort (imports)
echo ""
echo "📦 Verificando ordenamiento de imports con isort..."
if isort --check-only --diff . ; then
    success "Imports ordenados correctamente"
else
    error "Imports desordenados"
    warning "Ejecuta 'isort .' para corregir"
    exit 1
fi

# Paso 4: Flake8 (linting)
echo ""
echo "🔍 Ejecutando Flake8..."
if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics ; then
    success "No se encontraron errores críticos"
else
    error "Errores críticos encontrados"
    exit 1
fi

# Paso 5: Bandit (seguridad)
echo ""
echo "🔒 Ejecutando análisis de seguridad con Bandit..."
if bandit -r . -f json -o bandit-report.json ; then
    success "Análisis de seguridad completado"
else
    warning "Algunas vulnerabilidades potenciales encontradas (ver bandit-report.json)"
fi

# Paso 6: Tests
echo ""
echo "🧪 Ejecutando tests..."
if pytest tests/ -v --cov=. --cov-report=term --cov-report=html ; then
    success "Todos los tests pasaron"
else
    error "Algunos tests fallaron"
    exit 1
fi

# Paso 7: Verificar cobertura
echo ""
echo "📊 Verificando cobertura de código..."
coverage report --fail-under=70 || warning "Cobertura menor al 70%"

# Paso 8: Build Docker (opcional)
echo ""
read -p "¿Deseas construir las imágenes Docker? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🐳 Construyendo imágenes Docker..."
    if docker-compose build ; then
        success "Imágenes construidas exitosamente"
    else
        error "Error al construir imágenes"
        exit 1
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
success "Pipeline CI local completado exitosamente!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Reportes generados:"
echo "  - Cobertura HTML: htmlcov/index.html"
echo "  - Bandit: bandit-report.json"
echo ""
