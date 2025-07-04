import grpc
from concurrent import futures
import logging
import drivers_pb2_grpc
from driver_controller import DriverService
from database import init_db
import os
from kafka_utils import DriverKafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("drivers-server")

def serve():
    init_db()
    # Inicializar Kafka Producer
    kafka_producer = DriverKafkaProducer()
    # Ejemplo: enviar un evento de arranque
    kafka_producer.send_driver_event({'type': 'SERVICE_STARTED'})
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drivers_pb2_grpc.add_DriverServiceServicer_to_server(DriverService(), server)
    port = os.getenv('DRIVER_SERVICE_PORT', '50055')
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Servidor de choferes escuchando en el puerto {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve() 