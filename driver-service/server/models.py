from mongoengine import Document, StringField, BooleanField, DateTimeField, IntField
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("drivers")

class Driver(Document):
    name = StringField(required=True)
    license_type = IntField(required=True)  # 0: Light, 1: Heavy, 2: Both
    availability = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow) 