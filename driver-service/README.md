# Microservicio de Choferes

Este microservicio gestiona el registro, consulta, actualización y asignación de choferes, validando compatibilidad con vehículos y rutas.

## Endpoints gRPC
- Registrar chofer
- Consultar chofer por ID
- Listar choferes (con filtros)
- Actualizar chofer
- Asignar chofer a ruta y vehículo

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
   python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/drivers.proto
   python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/vehicles.proto
   python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/routes.proto
   ```
3. Levanta el servicio:
   ```bash
   python server/server.py
   ```

## Logging
El microservicio utiliza logging para registrar operaciones y errores relevantes. 