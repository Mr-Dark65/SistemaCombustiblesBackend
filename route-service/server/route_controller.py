import grpc
import logging
from models import Route
import routes_pb2, routes_pb2_grpc
from mongoengine.errors import DoesNotExist
import os
from kafka_utils import RouteKafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("routes-controller")

# Configuración del host del microservicio de vehículos
def get_vehicle_stub():
    vehicle_host = os.getenv('VEHICLE_SERVICE_HOST', 'vehicle-service:50052')
    channel = grpc.insecure_channel(vehicle_host)
    import vehicles_pb2_grpc, vehicles_pb2
    return vehicles_pb2_grpc.VehiclesServiceStub(channel), vehicles_pb2

class RouteService(routes_pb2_grpc.RouteServiceServicer):
    def __init__(self):
        super().__init__()
        self.kafka_producer = RouteKafkaProducer()

    def CreateRoute(self, request, context):
        logger.info(f"Creando ruta: {request.origin} -> {request.destination}, {request.distance} km")
        route = Route(
            origin=request.origin,
            destination=request.destination,
            distance=request.distance
        )
        route.save()
        # Enviar evento Kafka
        self.kafka_producer.send_route_event({
            "type": "CREATED",
            "entity": "route",
            "data": {
                "id": str(route.id),
                "origin": route.origin,
                "destination": route.destination,
                "distance": route.distance
            }
        })
        return routes_pb2.RouteResponse(
            id=str(route.id),
            origin=route.origin,
            destination=route.destination,
            distance=route.distance,
            vehicle_id=route.vehicle_id or ""
        )

    def GetRoute(self, request, context):
        try:
            route = Route.objects.get(id=request.id)
            logger.info(f"Consultando ruta: {route.id}")
            return routes_pb2.RouteResponse(
                id=str(route.id),
                origin=route.origin,
                destination=route.destination,
                distance=route.distance,
                vehicle_id=route.vehicle_id or ""
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ruta no encontrada")
            logger.warning(f"Ruta no encontrada: {request.id}")
            return routes_pb2.RouteResponse()

    def ListRoutes(self, request, context):
        logger.info("Listando todas las rutas")
        routes = Route.objects()
        return routes_pb2.ListRoutesResponse(
            routes=[routes_pb2.RouteResponse(
                id=str(r.id),
                origin=r.origin,
                destination=r.destination,
                distance=r.distance,
                vehicle_id=r.vehicle_id or ""
            ) for r in routes]
        )

    def UpdateRoute(self, request, context):
        try:
            route = Route.objects.get(id=request.id)
            logger.info(f"Actualizando ruta: {route.id}")
            route.origin = request.origin
            route.destination = request.destination
            route.distance = request.distance
            route.save()
            # Enviar evento Kafka
            self.kafka_producer.send_route_event({
                "type": "UPDATED",
                "entity": "route",
                "data": {
                    "id": str(route.id),
                    "origin": route.origin,
                    "destination": route.destination,
                    "distance": route.distance
                }
            })
            return routes_pb2.RouteResponse(
                id=str(route.id),
                origin=route.origin,
                destination=route.destination,
                distance=route.distance,
                vehicle_id=route.vehicle_id or ""
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ruta no encontrada")
            logger.warning(f"Ruta no encontrada para actualizar: {request.id}")
            return routes_pb2.RouteResponse()

    def AssignRouteToVehicle(self, request, context):
        try:
            route = Route.objects.get(id=request.route_id)
            logger.info(f"Asignando ruta {route.id} al vehículo {request.vehicle_id}")
            route.vehicle_id = request.vehicle_id
            route.save()
            # Enviar evento Kafka
            self.kafka_producer.send_route_event({
                "type": "ASSIGNED_VEHICLE",
                "entity": "route",
                "data": {
                    "id": str(route.id),
                    "vehicle_id": route.vehicle_id
                }
            })
            return routes_pb2.RouteResponse(
                id=str(route.id),
                origin=route.origin,
                destination=route.destination,
                distance=route.distance,
                vehicle_id=route.vehicle_id or ""
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ruta no encontrada")
            logger.warning(f"Ruta no encontrada para asignar vehículo: {request.route_id}")
            return routes_pb2.RouteResponse()

    def CalculateFuelConsumption(self, request, context):
        try:
            route = Route.objects.get(id=request.route_id)
            if not route.vehicle_id:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("La ruta no tiene vehículo asignado")
                logger.warning(f"Ruta sin vehículo asignado: {route.id}")
                return routes_pb2.FuelConsumptionResponse()
            # Obtener tipo de vehículo desde vehicle-service
            vehicle_stub, vehicles_pb2 = get_vehicle_stub()
            v_res = vehicle_stub.GetVehicle(vehicles_pb2.GetVehicleRequest(id=route.vehicle_id))
            tipo = v_res.type
            logger.info(f"Calculando consumo para ruta {route.id} y vehículo {route.vehicle_id} (tipo: {tipo})")
            # Fórmulas de ejemplo:
            if tipo == "Liviana":
                consumo = route.distance * 0.08  # 8 litros cada 100km
            elif tipo == "Pesada":
                consumo = route.distance * 0.25  # 25 litros cada 100km
            else:
                consumo = route.distance * 0.1  # Default
            return routes_pb2.FuelConsumptionResponse(
                estimated_consumption=consumo,
                unit="litros"
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ruta no encontrada")
            logger.warning(f"Ruta no encontrada para calcular consumo: {request.route_id}")
            return routes_pb2.FuelConsumptionResponse()
        except grpc.RpcError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error al consultar vehículo: {e}")
            logger.error(f"Error al consultar vehículo: {e}")
            return routes_pb2.FuelConsumptionResponse() 