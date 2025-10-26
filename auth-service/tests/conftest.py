"""
Configuración y fixtures compartidos para tests
"""
import pytest
import os
from unittest.mock import Mock


@pytest.fixture(scope="session")
def test_db_config():
    """Configuración de base de datos para tests"""
    return {
        "host": os.getenv("TEST_DB_HOST", "localhost"),
        "port": int(os.getenv("TEST_DB_PORT", "27017")),
        "username": os.getenv("TEST_DB_USER", "test"),
        "password": os.getenv("TEST_DB_PASSWORD", "test"),
        "database": "test_auth_service"
    }


@pytest.fixture
def mock_database():
    """Mock de la base de datos"""
    db = Mock()
    return db


@pytest.fixture
def sample_user_data():
    """Datos de ejemplo de un usuario"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123!",
        "role": "Operador"
    }


@pytest.fixture
def sample_jwt_secret():
    """Secret para JWT en tests"""
    return "test_secret_key_for_testing_only"


# Configuración de pytest
def pytest_configure(config):
    """Configuración inicial de pytest"""
    config.addinivalue_line(
        "markers", "unit: marca tests como tests unitarios"
    )
    config.addinivalue_line(
        "markers", "integration: marca tests como tests de integración"
    )
    config.addinivalue_line(
        "markers", "slow: marca tests que son lentos"
    )
