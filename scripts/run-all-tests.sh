#!/bin/bash

# Script para ejecutar tests de todos los servicios

echo "🧪 Ejecutando tests de todos los servicios..."

services=(
    "auth-service"
    "vehicle-service"
    "route-service"
    "fuel-consumption-service"
    "driver-service"
    "api-gateway"
)

failed_services=()
passed_services=()

for service in "${services[@]}"; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Testing: $service"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ -d "$service/tests" ]; then
        cd "$service"
        
        # Instalar dependencias si es necesario
        if [ -f "requirements.txt" ]; then
            pip install -q -r requirements.txt
            pip install -q pytest pytest-cov pytest-asyncio pytest-mock
        fi
        
        # Ejecutar tests
        if pytest tests/ -v --cov=. --cov-report=term ; then
            passed_services+=("$service")
            echo "✅ $service: PASSED"
        else
            failed_services+=("$service")
            echo "❌ $service: FAILED"
        fi
        
        cd ..
    else
        echo "⚠️  No se encontró directorio de tests para $service"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "RESUMEN DE TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ${#passed_services[@]} -gt 0 ]; then
    echo "✅ Servicios que pasaron (${#passed_services[@]}):"
    for service in "${passed_services[@]}"; do
        echo "   - $service"
    done
fi

if [ ${#failed_services[@]} -gt 0 ]; then
    echo ""
    echo "❌ Servicios que fallaron (${#failed_services[@]}):"
    for service in "${failed_services[@]}"; do
        echo "   - $service"
    done
    exit 1
else
    echo ""
    echo "🎉 Todos los tests pasaron exitosamente!"
    exit 0
fi
