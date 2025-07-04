FROM python:3.9-slim

WORKDIR /app

# Instalar compilador protobuf
RUN apt-get update && \
    apt-get install -y protobuf-compiler && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear carpeta 'generated' y archivo __init__.py para que sea un paquete Python
RUN mkdir -p generated && touch generated/__init__.py

# Generar stubs gRPC en carpeta generated
RUN python -m grpc_tools.protoc -I./protos \
    --python_out=./generated \
    --grpc_python_out=./generated \
    ./protos/auth.proto

# Asegurar que Python encuentre el módulo 'generated'
ENV PYTHONPATH=/app:/app/generated

# Variables de entorno
ENV DB_HOST=mongodb
ENV DB_NAME=auth_service
ENV JWT_SECRET=${JWT_SECRET}
ENV MONGO_ROOT_USERNAME=${MONGO_ROOT_USER}
ENV MONGO_ROOT_PASSWORD=${MONGO_ROOT_PASSWORD}

EXPOSE 50051

CMD ["python", "server/server.py"]
