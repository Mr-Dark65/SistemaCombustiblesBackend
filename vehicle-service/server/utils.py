import grpc
from datetime import datetime
from mongoengine import ValidationError
from enum import Enum
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VehicleType(str, Enum):
    LIGHT = "Liviana"
    HEAVY = "Pesada"

class VehicleStatus(str, Enum):
    AVAILABLE = "Disponible"
    IN_USE = "En uso"
    MAINTENANCE = "En mantenimiento"
    DISABLED = "Deshabilitado"

def validate_plate_number(plate: str) -> bool:
    """
    Valida el formato de la placa del vehículo
    Formato esperado: ABC123 o ABC1234 (dependiendo del país)
    """
    if len(plate) < 6 or len(plate) > 7:
        raise ValidationError("La placa debe tener entre 6 y 7 caracteres")
    
    # Validación básica - puede adaptarse según requisitos
    if not plate[:3].isalpha() or not plate[3:].isdigit():
        raise ValidationError("Formato de placa inválido. Ejemplo correcto: ABC123")
    
    return True

def validate_vehicle_year(year: int) -> bool:
    """
    Valida que el año del vehículo sea razonable
    """
    current_year = datetime.now().year
    if year < 1900 or year > current_year + 1:  # +1 para vehículos del próximo año
        raise ValidationError(f"El año debe estar entre 1900 y {current_year + 1}")
    return True

def handle_grpc_error(context: grpc.ServicerContext, error: Exception, error_message: str = "Error en el servicio"):
    """
    Maneja errores y los envía como respuesta gRPC
    """
    logger.error(f"{error_message}: {str(error)}")
    
    if isinstance(error, ValidationError):
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
    elif isinstance(error, ValueError):
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
    elif isinstance(error, LookupError):
        context.set_code(grpc.StatusCode.NOT_FOUND)
    else:
        context.set_code(grpc.StatusCode.INTERNAL)
    
    context.set_details(str(error))
    return None

def vehicle_to_dict(vehicle) -> dict:
    """
    Convierte un objeto Vehicle de MongoEngine a un diccionario
    """
    return {
        "id": str(vehicle.id),
        "plate": vehicle.plate,
        "type": vehicle.type,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "status": vehicle.status,
        "assigned_driver": str(vehicle.assigned_driver) if vehicle.assigned_driver else None,
        "created_at": vehicle.created_at.isoformat() if vehicle.created_at else None
    }

def build_vehicle_filter(
    type_filter: str = None,
    status_filter: str = None,
    driver_filter: str = None,
    min_year: int = None,
    max_year: int = None
) -> dict:
    """
    Construye un filtro de consulta para vehículos basado en los parámetros
    """
    query = {}
    
    if type_filter:
        query["type"] = type_filter
    if status_filter:
        query["status"] = status_filter
    if driver_filter:
        query["assigned_driver"] = driver_filter
    if min_year is not None:
        query["year__gte"] = min_year
    if max_year is not None:
        query["year__lte"] = max_year
    
    return query

def log_vehicle_operation(operation: str, vehicle_id: str, user: str = None):
    """
    Registra operaciones importantes sobre vehículos
    """
    log_message = f"Operación '{operation}' en vehículo {vehicle_id}"
    if user:
        log_message += f" por usuario {user}"
    logger.info(log_message)