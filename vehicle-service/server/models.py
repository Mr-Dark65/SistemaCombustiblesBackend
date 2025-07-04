from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField
from datetime import datetime

class Vehicle(Document):
    plate = StringField(required=True, unique=True)
    type = StringField(required=True, choices=["Liviana", "Pesada"])
    brand = StringField(required=True)
    model = StringField(required=True)
    year = IntField(required=True, min_value=2000, max_value=datetime.now().year)
    status = StringField(
        required=True,
        default="Disponible",
        choices=["Disponible", "En uso", "En mantenimiento", "Deshabilitado"]
    )
    assigned_driver = StringField()  # Referencia al ID del chofer
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'vehicles',
        'indexes': [
            'plate',
            'type',
            'status',
            'assigned_driver'
        ]
    }