from kafka import KafkaConsumer
import json
import os
import threading

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle-events')
ROUTE_TOPIC = os.getenv('ROUTE_TOPIC', 'route-events')

class VehicleKafkaConsumer(threading.Thread):
    def __init__(self, on_message):
        super().__init__()
        self.consumer = KafkaConsumer(
            VEHICLE_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='fuel-service-vehicle-group',
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.on_message = on_message
        self.daemon = True

    def run(self):
        for message in self.consumer:
            self.on_message(message.value)

class RouteKafkaConsumer(threading.Thread):
    def __init__(self, on_message):
        super().__init__()
        self.consumer = KafkaConsumer(
            ROUTE_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='fuel-service-route-group',
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.on_message = on_message
        self.daemon = True

    def run(self):
        for message in self.consumer:
            self.on_message(message.value)

# Ejemplo de uso:
# def handle_vehicle_event(event):
#     print('Evento de vehículo recibido:', event)
# def handle_route_event(event):
#     print('Evento de ruta recibido:', event)
# vehicle_consumer = VehicleKafkaConsumer(handle_vehicle_event)
# route_consumer = RouteKafkaConsumer(handle_route_event)
# vehicle_consumer.start()
# route_consumer.start() 