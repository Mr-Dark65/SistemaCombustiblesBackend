from mongoengine import Document, StringField, FloatField, DateTimeField
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fuel")

class FuelConsumption(Document):
    route_id = StringField(required=True)
    vehicle_id = StringField(required=True)
    fuel_amount = FloatField(required=True)
    created_at = DateTimeField(default=datetime.utcnow) 