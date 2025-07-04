import grpc
from concurrent import futures
import logging
import fuel_pb2_grpc
from fuel_controller import FuelService
from database import init_db
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fuel-server")

def serve():
    init_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fuel_pb2_grpc.add_FuelServiceServicer_to_server(FuelService(), server)
    port = os.getenv('FUEL_SERVICE_PORT', '50054')
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Servidor de consumo de combustible escuchando en el puerto {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve() 