import grpc
from concurrent import futures
import logging
import routes_pb2_grpc
from route_controller import RouteService
from database import init_db
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("routes-server")

def serve():
    init_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    routes_pb2_grpc.add_RouteServiceServicer_to_server(RouteService(), server)
    port = os.getenv('ROUTE_SERVICE_PORT', '50053')
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Servidor de rutas escuchando en el puerto {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve() 