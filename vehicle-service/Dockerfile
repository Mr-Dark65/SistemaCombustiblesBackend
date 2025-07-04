FROM python:3.9-slim

WORKDIR /app

# Instalar compilador protobuf y herramientas necesarias
RUN apt-get update && \
    apt-get install -y protobuf-compiler build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copiar solo los requirements para aprovechar cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente
COPY . .

# Crear carpeta 'generated' y generar los stubs gRPC
RUN mkdir -p generated && \
    python -m grpc_tools.protoc \
        -I./protos \
        --python_out=./generated \
        --grpc_python_out=./generated \
        ./protos/vehicles.proto && \
    touch generated/__init__.py

# Añadir carpetas al PYTHONPATH
ENV PYTHONPATH=/app:/app/generated:/app/server

# Variables de entorno
ENV DB_HOST=mongodb
ENV DB_NAME=vehicle_service
ENV MONGO_ROOT_USERNAME=${MONGO_ROOT_USER}
ENV MONGO_ROOT_PASSWORD=${MONGO_ROOT_PASSWORD}

EXPOSE 50052

CMD ["python", "server/server.py"]
