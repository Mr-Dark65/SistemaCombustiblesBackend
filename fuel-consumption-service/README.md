# Microservicio de Consumo de Combustible

Este microservicio gestiona el registro y consulta de consumos de combustible, permitiendo reportes y comparaciones con el consumo estimado.

## Endpoints gRPC
- Registrar consumo real
- Consultar consumo por ID
- Listar consumos (con filtros)
- Reporte por tipo de maquinaria
- Comparar consumo estimado vs real

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
   python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/fuel.proto
   python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/vehicles.proto
   python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/routes.proto
   ```
3. Levanta el servicio:
   ```bash
   python server/server.py
   ```

## Logging
El microservicio utiliza logging para registrar operaciones y errores relevantes. 