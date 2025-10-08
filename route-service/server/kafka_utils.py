from kafka import KafkaProducer, KafkaConsumer
import json
import os
import threading

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle-events')
ROUTE_TOPIC = os.getenv('ROUTE_TOPIC', 'route-events')

class RouteKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_route_event(self, event: dict):
        self.producer.send(ROUTE_TOPIC, event)
        self.producer.flush()

class VehicleKafkaConsumer(threading.Thread):
    def __init__(self, on_message):
        super().__init__()
        self.consumer = KafkaConsumer(
            VEHICLE_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='route-service-group',
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
# consumer = VehicleKafkaConsumer(handle_vehicle_event)
# consumer.start()
# producer = RouteKafkaProducer()
# producer.send_route_event({'type': 'CREATED', 'route_id': 'xyz', ...}) 