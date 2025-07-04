import grpc
import logging
from models import Driver
import drivers_pb2, drivers_pb2_grpc
from mongoengine.errors import DoesNotExist
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("drivers-controller")

# Stubs externos
def get_vehicle_stub():
    vehicle_host = os.getenv('VEHICLE_SERVICE_HOST', 'vehicle-service:50052')
    from vehicles_pb2_grpc import VehiclesServiceStub
    import vehicles_pb2
    channel = grpc.insecure_channel(vehicle_host)
    return VehiclesServiceStub(channel), vehicles_pb2

def get_route_stub():
    route_host = os.getenv('ROUTE_SERVICE_HOST', 'route-service:50053')
    from routes_pb2_grpc import RouteServiceStub
    import routes_pb2
    channel = grpc.insecure_channel(route_host)
    return RouteServiceStub(channel), routes_pb2

class DriverService(drivers_pb2_grpc.DriverServiceServicer):
    def RegisterDriver(self, request, context):
        logger.info(f"Registrando chofer: {request.name}, licencia: {request.license_type}, disponible: {request.availability}")
        driver = Driver(
            name=request.name,
            license_type=request.license_type,
            availability=request.availability,
            created_at=datetime.utcnow()
        )
        driver.save()
        return drivers_pb2.DriverResponse(
            id=str(driver.id),
            name=driver.name,
            license_type=driver.license_type,
            availability=driver.availability,
            created_at=driver.created_at.isoformat()
        )

    def GetDriver(self, request, context):
        try:
            driver = Driver.objects.get(id=request.id)
            logger.info(f"Consultando chofer: {driver.id}")
            return drivers_pb2.DriverResponse(
                id=str(driver.id),
                name=driver.name,
                license_type=driver.license_type,
                availability=driver.availability,
                created_at=driver.created_at.isoformat()
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Chofer no encontrado")
            logger.warning(f"Chofer no encontrado: {request.id}")
            return drivers_pb2.DriverResponse()

    def ListDrivers(self, request, context):
        logger.info("Listando choferes")
        query = {}
        if request.HasField('availability'):
            query['availability'] = request.availability
        if request.HasField('license_type'):
            query['license_type'] = request.license_type
        drivers = Driver.objects(**query)
        return drivers_pb2.ListDriversResponse(
            drivers=[drivers_pb2.DriverResponse(
                id=str(d.id),
                name=d.name,
                license_type=d.license_type,
                availability=d.availability,
                created_at=d.created_at.isoformat()
            ) for d in drivers]
        )

    def UpdateDriver(self, request, context):
        try:
            driver = Driver.objects.get(id=request.id)
            logger.info(f"Actualizando chofer: {driver.id}")
            driver.name = request.name
            driver.license_type = request.license_type
            driver.availability = request.availability
            driver.save()
            return drivers_pb2.DriverResponse(
                id=str(driver.id),
                name=driver.name,
                license_type=driver.license_type,
                availability=driver.availability,
                created_at=driver.created_at.isoformat()
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Chofer no encontrado")
            logger.warning(f"Chofer no encontrado para actualizar: {request.id}")
            return drivers_pb2.DriverResponse()

    def AssignDriver(self, request, context):
        try:
            driver = Driver.objects.get(id=request.driver_id)
            logger.info(f"Asignando chofer {driver.id} a ruta {request.route_id} y vehículo {request.vehicle_id}")
            # Validar disponibilidad
            if not driver.availability:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("Chofer no disponible")
                logger.warning(f"Chofer no disponible: {driver.id}")
                return drivers_pb2.AssignDriverResponse(success=False, message="Chofer no disponible")
            # Validar tipo de licencia vs tipo de vehículo
            vehicle_stub, vehicles_pb2 = get_vehicle_stub()
            v_res = vehicle_stub.GetVehicle(vehicles_pb2.GetVehicleRequest(id=request.vehicle_id))
            tipo = v_res.type
            if (tipo == "Liviana" and driver.license_type not in [0,2]) or (tipo == "Pesada" and driver.license_type not in [1,2]):
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("Chofer no calificado para el tipo de vehículo")
                logger.warning(f"Chofer {driver.id} no calificado para vehículo {request.vehicle_id} ({tipo})")
                return drivers_pb2.AssignDriverResponse(success=False, message="Chofer no calificado para el tipo de vehículo")
            # Marcar chofer como no disponible
            driver.availability = False
            driver.save()
            # (Opcional) Actualizar la ruta con el chofer asignado
            # route_stub, routes_pb2 = get_route_stub()
            # route_stub.UpdateRouteWithDriver(routes_pb2.UpdateRouteWithDriverRequest(route_id=request.route_id, driver_id=str(driver.id)))
            return drivers_pb2.AssignDriverResponse(success=True, message="Chofer asignado correctamente")
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Chofer no encontrado")
            logger.warning(f"Chofer no encontrado para asignar: {request.driver_id}")
            return drivers_pb2.AssignDriverResponse(success=False, message="Chofer no encontrado")
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error al consultar vehículo: {e}")
            logger.error(f"Error al consultar vehículo: {e}")
            return drivers_pb2.AssignDriverResponse(success=False, message="Error al consultar vehículo") 