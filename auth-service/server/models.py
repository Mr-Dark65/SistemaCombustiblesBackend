from mongoengine import Document, StringField
from mongoengine.errors import ValidationError

def validate_role(value):
    valid_roles = ['Admin', 'Operador', 'Supervisor']
    if value not in valid_roles:
        raise ValidationError(f'Rol inválido. Debe ser uno de: {", ".join(valid_roles)}')

class User(Document):
    username = StringField(required=True, unique=True, max_length=50)
    password = StringField(required=True)
    email = StringField(required=True, unique=True)
    role = StringField(required=True, validation=validate_role)
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'email']
    }