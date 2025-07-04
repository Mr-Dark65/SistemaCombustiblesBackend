from mongoengine import Document, StringField, FloatField
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("routes")

class Route(Document):
    origin = StringField(required=True)
    destination = StringField(required=True)
    distance = FloatField(required=True)
    vehicle_id = StringField() 