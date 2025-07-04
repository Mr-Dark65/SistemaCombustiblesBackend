# Backend Microservicios - Gestión de Vehículos, Rutas, Consumo y Choferes

Este proyecto implementa un sistema de gestión de flotas basado en microservicios, utilizando Python, gRPC, FastAPI y MongoDB, orquestado con Docker Compose. Incluye autenticación, gestión de vehículos, rutas, consumo de combustible y choferes, todo accesible de forma segura a través de un API Gateway.

## Arquitectura

- **API Gateway**: Expone una API REST (FastAPI) que unifica y protege el acceso a los microservicios, validando tokens y roles.
- **auth-service**: Servicio de autenticación y autorización (gRPC, JWT, MongoDB).
- **vehicle-service**: Gestión de vehículos y asignación de choferes (gRPC, MongoDB).
- **route-service**: Gestión de rutas y asociación con vehículos (gRPC, MongoDB).
- **fuel-consumption-service**: Registro y consulta de consumos de combustible, reportes y comparaciones (gRPC, MongoDB).
- **driver-service**: Registro, consulta, actualización y asignación de choferes (gRPC, MongoDB).
- **MongoDB**: Base de datos centralizada para todos los servicios.

## Tecnologías principales

- Python 3.9+
- FastAPI (API Gateway)
- gRPC (comunicación entre servicios)
- MongoDB (persistencia)
- Docker & Docker Compose (orquestación)
- Protobuf (definición de contratos)
- JWT (autenticación)

## Estructura del repositorio

```
Backend/
  ├── api-gateway/
  ├── auth-service/
  ├── vehicle-service/
  ├── route-service/
  ├── fuel-consumption-service/
  ├── driver-service/
  └── docker-compose.yml
```

## Despliegue rápido

1. **Clona el repositorio y navega a la carpeta Backend:**
   ```bash
   git clone <repo_url>
   cd Backend
   ```

2. **Configura variables de entorno (opcional):**
   - Puedes definir `MONGO_ROOT_USER`, `MONGO_ROOT_PASSWORD`, `JWT_SECRET` en un archivo `.env` o en tu entorno.

3. **Levanta todos los servicios con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Accede a la API REST:**
   - Documentación Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
   - La API Gateway escucha en el puerto `8000`.

## Servicios y puertos

| Servicio                   | Puerto | Descripción                                 |
|----------------------------|--------|---------------------------------------------|
| MongoDB                    | 27017  | Base de datos                               |
| auth-service               | 50051  | Autenticación y JWT                         |
| vehicle-service            | 50052  | Gestión de vehículos                        |
| route-service              | 50053  | Gestión de rutas                            |
| fuel-consumption-service   | 50054  | Consumo de combustible                      |
| driver-service             | 50055  | Gestión de choferes                         |
| api-gateway                | 8000   | API REST unificada                          |

## Endpoints principales

- **Autenticación:** `/register`, `/login`, `/validate-token`
- **Vehículos:** `/vehicles`, `/vehicles/{id}`, `/vehicles/{id}/status`, `/vehicles/{id}/assign-driver`
- **Rutas:** `/routes`, `/routes/{id}`, `/routes/{id}/assign-vehicle`, `/routes/{id}/fuel-consumption`
- **Consumo de combustible:** `/fuel`, `/fuel/{id}`, `/fuel/report/by-vehicle-type`, `/fuel/compare/{route_id}`
- **Choferes:** `/drivers`, `/drivers/{id}`, `/drivers/{id}/assign`

> Todos los endpoints (excepto login y register) requieren autenticación mediante token JWT.

## Desarrollo y pruebas locales

- Cada microservicio tiene su propio `README.md` con instrucciones para desarrollo y pruebas individuales.
- Para modificar los contratos gRPC, edita los archivos `.proto` correspondientes y regenera los stubs con:
  ```bash
  python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos/<archivo>.proto
  ```

## Seguridad y control de acceso

- El API Gateway valida el token JWT en cada petición y controla el acceso según el rol (`Admin`, `Operador`, `Supervisor`).
- Los roles determinan qué operaciones puede realizar cada usuario en los distintos servicios.

## Logging

- Todos los microservicios implementan logging para registrar operaciones y errores relevantes.

## Notas adicionales

- El sistema está preparado para escalar y agregar nuevos microservicios fácilmente.
- Puedes extender la lógica de negocio, los modelos y los endpoints según las necesidades de tu organización. 