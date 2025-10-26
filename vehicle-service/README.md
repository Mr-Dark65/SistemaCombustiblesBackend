Vehicle Service
===============

Política de eliminación (DeleteVehicle)
--------------------------------------

Este servicio expone la RPC `DeleteVehicle(DeleteVehicleRequest) -> VehicleResponse`.

- Por defecto la eliminación es "soft delete" (campo `soft = true` o cuando no se envía `soft`).
- Soft delete:
  - Se establece `deleted_at` con la fecha/hora UTC actual.
  - El campo `status` se actualiza a `Deshabilitado`.
  - El documento se mantiene en la colección para auditoría y posible restauración.
- Hard delete (`soft = false`): el documento se elimina físicamente de la base de datos.

Cómo revertir un soft delete
---------------------------

Puedes revertir un soft delete restableciendo `deleted_at = None` y actualizando `status` a un valor válido, por ejemplo `Disponible`.

Ejemplo (pseudocódigo Python usando mongoengine):

```python
from server.models import Vehicle
v = Vehicle.objects(id='...').first()
if v and v.deleted_at:
    v.deleted_at = None
    v.status = 'Disponible'
    v.save()
```

Eventos Kafka
-------------

El servicio publica eventos Kafka para acciones importantes:
- `CREATED`, `UPDATED_STATUS`, `ASSIGNED_DRIVER`, `REMOVED_DRIVER`, `DELETED_SOFT`, `DELETED_HARD`

Pruebas rápidas
---------------

Generar stubs protobuf (si modificaste `protos/vehicles.proto`):

```powershell
Set-Location '...\vehicle-service'
python -m grpc_tools.protoc -I=protos --python_out=server --grpc_python_out=server protos\vehicles.proto
```

Comando para iniciar el servidor (ajusta variables de entorno según sea necesario):

```powershell
$env:PYTHONPATH = "$PWD\server;$PWD"
python .\server\server.py
```

Luego puedes llamar a `DeleteVehicle` con grpcurl o un cliente gRPC.
