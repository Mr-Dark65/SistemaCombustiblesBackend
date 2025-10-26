"""
Fixtures compartidos para tests del API Gateway
"""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_grpc_stub():
    """Mock de stub gRPC"""
    stub = Mock()
    return stub


@pytest.fixture
def sample_auth_token():
    """Token de autenticación de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"


@pytest.fixture
def sample_request_headers(sample_auth_token):
    """Headers de ejemplo para requests"""
    return {
        "Authorization": f"Bearer {sample_auth_token}"
    }
