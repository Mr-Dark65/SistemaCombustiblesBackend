from mongoengine import connect
import os

def init_db():
    db_host = os.getenv('DB_HOST', 'mongodb')
    db_name = os.getenv('DB_NAME', 'vehicle_service')
    db_user = os.getenv('MONGO_ROOT_USERNAME', 'root')
    db_pass = os.getenv('MONGO_ROOT_PASSWORD', 'example')
    
    connect(
        db=db_name,
        host=f'mongodb://{db_user}:{db_pass}@{db_host}:27017/{db_name}?authSource=admin',
        alias='default'
    )
    print(f"Conectado a MongoDB en {db_host}, base de datos: {db_name}")