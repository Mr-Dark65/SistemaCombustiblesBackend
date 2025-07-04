# API Gateway

Este servicio expone una API REST que unifica y protege el acceso a los microservicios de autenticación y vehículos.

## Tecnologías
- FastAPI
- gRPC (cliente)

## Uso

1. Asegúrate de tener los microservicios corriendo (auth-service y vehicle-service).
2. Levanta el gateway con Docker Compose:

```bash
docker-compose up --build
```

La API estará disponible en http://localhost:8000 