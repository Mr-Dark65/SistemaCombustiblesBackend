# Microservicio de Rutas

Este microservicio gestiona rutas y su asociación con vehículos, permitiendo calcular el consumo estimado de combustible.

## Endpoints gRPC
- Crear ruta
- Consultar ruta por ID
- Listar rutas
- Actualizar ruta
- Asociar ruta a vehículo
- Calcular consumo de combustible

## Dependencias
- MongoDB
- grpcio, grpcio-tools, mongoengine

## Uso

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Genera los stubs gRPC si modificas el proto:
   ```bash
   python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/routes.proto
   ```
3. Levanta el servicio:
   ```bash
   python server/server.py
   ```

## Logging
El microservicio utiliza logging para registrar operaciones y errores relevantes. 