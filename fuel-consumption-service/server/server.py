import grpc
from concurrent import futures
import logging
import fuel_pb2_grpc
from fuel_controller import FuelService
from database import init_db
import os
from kafka_utils import VehicleKafkaConsumer, RouteKafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fuel-server")

def serve():
    init_db()
    # Inicializar Kafka Consumers
    def handle_vehicle_event(event):
        print('Evento de vehículo recibido en fuel-consumption-service:', event)
    def handle_route_event(event):
        print('Evento de ruta recibido en fuel-consumption-service:', event)
    vehicle_consumer = VehicleKafkaConsumer(handle_vehicle_event)
    route_consumer = RouteKafkaConsumer(handle_route_event)
    vehicle_consumer.start()
    route_consumer.start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fuel_pb2_grpc.add_FuelServiceServicer_to_server(FuelService(), server)
    port = os.getenv('FUEL_SERVICE_PORT', '50054')
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Servidor de consumo de combustible escuchando en el puerto {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve() 