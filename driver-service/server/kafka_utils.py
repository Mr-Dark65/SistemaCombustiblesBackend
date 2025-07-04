from kafka import KafkaProducer
import json
import os

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
DRIVER_TOPIC = os.getenv('DRIVER_TOPIC', 'driver-events')

class DriverKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_driver_event(self, event: dict):
        self.producer.send(DRIVER_TOPIC, event)
        self.producer.flush()

# Ejemplo de uso:
# producer = DriverKafkaProducer()
# producer.send_driver_event({'type': 'CREATED', 'driver_id': 'abc', ...}) 