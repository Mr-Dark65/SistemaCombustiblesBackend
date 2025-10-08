from kafka import KafkaConsumer
import json
import os
import threading

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
AUTH_TOPIC = os.getenv('AUTH_TOPIC', 'auth-events')

class AuthKafkaConsumer(threading.Thread):
    def __init__(self, on_message):
        super().__init__()
        self.consumer = KafkaConsumer(
            AUTH_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='auth-service-group',
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.on_message = on_message
        self.daemon = True

    def run(self):
        for message in self.consumer:
            self.on_message(message.value)

# Ejemplo de uso:
# def handle_auth_event(event):
#     print('Evento de autenticación recibido:', event)
# consumer = AuthKafkaConsumer(handle_auth_event)
# consumer.start() 