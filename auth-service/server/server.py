from concurrent import futures
import grpc
import logging
from database import init_db
from generated import auth_pb2_grpc
from auth_controller import AuthController
from kafka_utils import AuthKafkaConsumer

def serve():
    # Inicializar la base de datos
    init_db()
    # Inicializar Kafka Consumer para auditoría
    def handle_auth_event(event):
        print('Evento de autenticación recibido en auth-service:', event)
    kafka_consumer = AuthKafkaConsumer(handle_auth_event)
    kafka_consumer.start()
    # Configurar el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthController(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("AuthService escuchando en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()