import grpc
import vehicles_pb2
import vehicles_pb2_grpc
from models import Vehicle
from datetime import datetime
from kafka_utils import VehicleKafkaProducer

class VehicleController(vehicles_pb2_grpc.VehiclesServiceServicer):
    def __init__(self):
        super().__init__()
        self.kafka_producer = VehicleKafkaProducer()

    def CreateVehicle(self, request, context):
        try:
            # Validar tipo de vehículo
            if request.type not in ["Liviana", "Pesada"]:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Tipo de vehículo inválido. Debe ser 'Liviana' o 'Pesada'")
                return vehicles_pb2.VehicleResponse()
            
            # Crear nuevo vehículo
            vehicle = Vehicle(
                plate=request.plate,
                type=request.type,
                brand=request.brand,
                model=request.model,
                year=request.year,
                status="Disponible",
                created_at=datetime.utcnow()
            )
            vehicle.save()
            
            # Enviar evento Kafka
            self.kafka_producer.send_vehicle_event({
                "type": "CREATED",
                "entity": "vehicle",
                "data": {
                    "id": str(vehicle.id),
                    "plate": vehicle.plate,
                    "type": vehicle.type,
                    "brand": vehicle.brand,
                    "model": vehicle.model,
                    "year": vehicle.year,
                    "status": vehicle.status
                }
            })
            
            return vehicles_pb2.VehicleResponse(
                id=str(vehicle.id),
                plate=vehicle.plate,
                type=vehicle.type,
                status=vehicle.status,
                brand=vehicle.brand,
                model=vehicle.model,
                year=vehicle.year
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return vehicles_pb2.VehicleResponse()

    def GetVehicle(self, request, context):
        try:
            vehicle = Vehicle.objects(id=request.id).first()
            if not vehicle:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Vehículo no encontrado")
                return vehicles_pb2.VehicleResponse()
            
            return self._vehicle_to_response(vehicle)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return vehicles_pb2.VehicleResponse()

    def ListVehicles(self, request, context):
        try:
            query = {}
            if request.type_filter:
                query["type"] = request.type_filter
            if request.status_filter:
                query["status"] = request.status_filter
            
            vehicles = Vehicle.objects(**query)
            
            response = vehicles_pb2.ListVehiclesResponse()
            for vehicle in vehicles:
                response.vehicles.append(self._vehicle_to_response(vehicle))
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return vehicles_pb2.ListVehiclesResponse()

    def UpdateVehicleStatus(self, request, context):
        try:
            vehicle = Vehicle.objects(id=request.vehicle_id).first()
            if not vehicle:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Vehículo no encontrado")
                return vehicles_pb2.VehicleResponse()
            
            vehicle.status = request.new_status
            vehicle.save()
            
            # Enviar evento Kafka
            self.kafka_producer.send_vehicle_event({
                "type": "UPDATED_STATUS",
                "entity": "vehicle",
                "data": {
                    "id": str(vehicle.id),
                    "status": vehicle.status
                }
            })
            
            return self._vehicle_to_response(vehicle)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return vehicles_pb2.VehicleResponse()

    def AssignDriver(self, request, context):
        try:
            vehicle = Vehicle.objects(id=request.vehicle_id).first()
            if not vehicle:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Vehículo no encontrado")
                return vehicles_pb2.VehicleResponse()
            
            vehicle.assigned_driver = request.driver_id
            vehicle.save()
            
            # Enviar evento Kafka
            self.kafka_producer.send_vehicle_event({
                "type": "ASSIGNED_DRIVER",
                "entity": "vehicle",
                "data": {
                    "id": str(vehicle.id),
                    "assigned_driver": vehicle.assigned_driver
                }
            })
            
            return self._vehicle_to_response(vehicle)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return vehicles_pb2.VehicleResponse()

    def RemoveDriver(self, request, context):
        try:
            vehicle = Vehicle.objects(id=request.vehicle_id).first()
            if not vehicle:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Vehículo no encontrado")
                return vehicles_pb2.VehicleResponse()
            
            # Guardar el ID del chofer antes de removerlo para el evento
            removed_driver_id = vehicle.assigned_driver
            vehicle.assigned_driver = None
            vehicle.save()
            
            # Enviar evento Kafka
            self.kafka_producer.send_vehicle_event({
                "type": "REMOVED_DRIVER",
                "entity": "vehicle",
                "data": {
                    "id": str(vehicle.id),
                    "removed_driver": removed_driver_id
                }
            })
            
            return self._vehicle_to_response(vehicle)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return vehicles_pb2.VehicleResponse()

    def _vehicle_to_response(self, vehicle):
        response = vehicles_pb2.VehicleResponse(
            id=str(vehicle.id),
            plate=vehicle.plate,
            type=vehicle.type,
            status=vehicle.status,
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year
        )
        if vehicle.assigned_driver:
            response.assigned_driver = str(vehicle.assigned_driver)
        return response