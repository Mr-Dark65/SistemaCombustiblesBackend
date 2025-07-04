import grpc
import logging
from models import FuelConsumption
import fuel_pb2, fuel_pb2_grpc
from mongoengine.errors import DoesNotExist
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fuel-controller")

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

class FuelService(fuel_pb2_grpc.FuelServiceServicer):
    def RegisterFuelConsumption(self, request, context):
        logger.info(f"Registrando consumo: ruta={request.route_id}, vehiculo={request.vehicle_id}, litros={request.fuel_amount}")
        consumo = FuelConsumption(
            route_id=request.route_id,
            vehicle_id=request.vehicle_id,
            fuel_amount=request.fuel_amount,
            created_at=datetime.utcnow()
        )
        consumo.save()
        return fuel_pb2.FuelConsumptionResponse(
            id=str(consumo.id),
            route_id=consumo.route_id,
            vehicle_id=consumo.vehicle_id,
            fuel_amount=consumo.fuel_amount,
            created_at=consumo.created_at.isoformat()
        )

    def GetFuelConsumption(self, request, context):
        try:
            consumo = FuelConsumption.objects.get(id=request.id)
            logger.info(f"Consultando consumo: {consumo.id}")
            return fuel_pb2.FuelConsumptionResponse(
                id=str(consumo.id),
                route_id=consumo.route_id,
                vehicle_id=consumo.vehicle_id,
                fuel_amount=consumo.fuel_amount,
                created_at=consumo.created_at.isoformat()
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Consumo no encontrado")
            logger.warning(f"Consumo no encontrado: {request.id}")
            return fuel_pb2.FuelConsumptionResponse()

    def ListFuelConsumptions(self, request, context):
        logger.info("Listando consumos de combustible")
        query = {}
        if request.route_id:
            query['route_id'] = request.route_id
        if request.vehicle_id:
            query['vehicle_id'] = request.vehicle_id
        consumos = FuelConsumption.objects(**query)
        # Filtrar por tipo de maquinaria si es necesario
        if request.vehicle_type:
            vehicle_stub, vehicles_pb2 = get_vehicle_stub()
            consumos = [c for c in consumos if self._vehicle_type(c.vehicle_id, vehicle_stub, vehicles_pb2) == request.vehicle_type]
        return fuel_pb2.ListFuelConsumptionsResponse(
            consumptions=[fuel_pb2.FuelConsumptionResponse(
                id=str(c.id),
                route_id=c.route_id,
                vehicle_id=c.vehicle_id,
                fuel_amount=c.fuel_amount,
                created_at=c.created_at.isoformat()
            ) for c in consumos]
        )

    def ReportByVehicleType(self, request, context):
        logger.info(f"Reporte de consumo por tipo: {request.vehicle_type}")
        vehicle_stub, vehicles_pb2 = get_vehicle_stub()
        consumos = FuelConsumption.objects()
        filtrados = [c for c in consumos if self._vehicle_type(c.vehicle_id, vehicle_stub, vehicles_pb2) == request.vehicle_type]
        total = sum(c.fuel_amount for c in filtrados)
        return fuel_pb2.ReportByVehicleTypeResponse(
            total_fuel=total,
            count=len(filtrados),
            consumptions=[fuel_pb2.FuelConsumptionResponse(
                id=str(c.id),
                route_id=c.route_id,
                vehicle_id=c.vehicle_id,
                fuel_amount=c.fuel_amount,
                created_at=c.created_at.isoformat()
            ) for c in filtrados]
        )

    def CompareEstimatedVsReal(self, request, context):
        logger.info(f"Comparando consumo estimado vs real para ruta: {request.route_id}")
        # Consumo real
        consumos = FuelConsumption.objects(route_id=request.route_id)
        real = sum(c.fuel_amount for c in consumos)
        # Consumo estimado
        route_stub, routes_pb2 = get_route_stub()
        try:
            est_res = route_stub.CalculateFuelConsumption(routes_pb2.CalculateFuelConsumptionRequest(route_id=request.route_id, vehicle_id=""))
            estimated = est_res.estimated_consumption
            unit = est_res.unit
        except grpc.RpcError as e:
            logger.error(f"Error al consultar consumo estimado: {e}")
            estimated = 0.0
            unit = "litros"
        return fuel_pb2.CompareEstimatedVsRealResponse(
            estimated=estimated,
            real=real,
            unit=unit
        )

    def _vehicle_type(self, vehicle_id, vehicle_stub, vehicles_pb2):
        try:
            v_res = vehicle_stub.GetVehicle(vehicles_pb2.GetVehicleRequest(id=vehicle_id))
            return v_res.type
        except Exception as e:
            logger.warning(f"No se pudo obtener el tipo de vehículo {vehicle_id}: {e}")
            return "" 