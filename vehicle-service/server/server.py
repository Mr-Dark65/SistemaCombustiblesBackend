from concurrent import futures
import grpc
import logging
from database import init_db
from generated import vehicles_pb2_grpc
from vehicle_controller import VehicleController

def serve():
    # Inicializar la base de datos
    init_db()
    
    # Configurar el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vehicles_pb2_grpc.add_VehiclesServiceServicer_to_server(VehicleController(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("VehicleService escuchando en el puerto 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()