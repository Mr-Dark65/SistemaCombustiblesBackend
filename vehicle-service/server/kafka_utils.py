from kafka import KafkaProducer
import json
import os

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle-events')

class VehicleKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_vehicle_event(self, event: dict):
        self.producer.send(VEHICLE_TOPIC, event)
        self.producer.flush()

# Ejemplo de uso:
# producer = VehicleKafkaProducer()
# producer.send_vehicle_event({'type': 'CREATED', 'vehicle_id': '123', ...}) 