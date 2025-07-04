from fastapi import FastAPI, Depends, HTTPException, Header, status, Body, Query
from typing import Optional, List, Callable
import grpc
import auth_pb2, auth_pb2_grpc
import vehicles_pb2, vehicles_pb2_grpc
import routes_pb2, routes_pb2_grpc
import fuel_pb2, fuel_pb2_grpc
import drivers_pb2, drivers_pb2_grpc
from functools import wraps
from pydantic import BaseModel
import inspect
from enum import Enum

app = FastAPI(title="API Gateway")

# Service hosts
AUTH_SERVICE_HOST = "auth-service:50051"
VEHICLE_SERVICE_HOST = "vehicle-service:50052"
ROUTE_SERVICE_HOST = "route-service:50053"
FUEL_SERVICE_HOST = "fuel-consumption-service:50054"
DRIVER_SERVICE_HOST = "driver-service:50055"

# gRPC stubs
def get_auth_stub():
    channel = grpc.insecure_channel(AUTH_SERVICE_HOST)
    return auth_pb2_grpc.AuthServiceStub(channel)

def get_vehicles_stub():
    channel = grpc.insecure_channel(VEHICLE_SERVICE_HOST)
    return vehicles_pb2_grpc.VehiclesServiceStub(channel)

def get_route_stub():
    channel = grpc.insecure_channel(ROUTE_SERVICE_HOST)
    return routes_pb2_grpc.RouteServiceStub(channel)

def get_fuel_stub():
    channel = grpc.insecure_channel(FUEL_SERVICE_HOST)
    return fuel_pb2_grpc.FuelServiceStub(channel)

def get_driver_stub():
    channel = grpc.insecure_channel(DRIVER_SERVICE_HOST)
    return drivers_pb2_grpc.DriverServiceStub(channel)

# Context for token validation result
class TokenData:
    def __init__(self, role: str, user_id: str):
        self.role = role
        self.user_id = user_id

# Dependency to validate token
async def validate_token(token: str = Header(...)):
    auth_stub = get_auth_stub()
    try:
        token_res = auth_stub.ValidateToken(auth_pb2.TokenRequest(token=token))
        if not token_res.valid:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return TokenData(role=token_res.role, user_id=token_res.user_id)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Error de autenticación: " + str(e))

# Decorator to require valid token
def require_valid_token(endpoint: Callable):
    @wraps(endpoint)
    async def wrapper(*args, token_data: TokenData = Depends(validate_token), **kwargs):
        if inspect.iscoroutinefunction(endpoint):
            return await endpoint(*args, token_data=token_data, **kwargs)
        else:
            return endpoint(*args, token_data=token_data, **kwargs)
    return wrapper

@app.get("/", tags=["Admin"])
def root():
    return {"message": "API Gateway funcionando"}

@app.post("/register", tags=["Auth"])
def register(username: str, password: str, email: str, role: str):
    stub = get_auth_stub()
    req = auth_pb2.RegisterRequest(username=username, password=password, email=email, role=role)
    try:
        res = stub.Register(req)
        return {"success": res.success, "message": res.message, "user_id": res.user_id}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login", tags=["Auth"])
def login(username: str, password: str):
    stub = get_auth_stub()
    req = auth_pb2.LoginRequest(username=username, password=password)
    try:
        res = stub.Login(req)
        if not res.success:
            raise HTTPException(status_code=401, detail=res.message)
        return {"token": res.token, "role": res.role, "message": res.message}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-token", tags=["Auth"])
def validate_token_endpoint(token_data: TokenData = Depends(validate_token)):
    return {"valid": True, "role": token_data.role, "user_id": token_data.user_id}

# --- VEHICLES ---
@app.post("/vehicles", tags=["vehicles"])
@require_valid_token
def create_vehicle(plate: str, type: str, brand: str, model: str, year: int, token_data: TokenData = Depends(validate_token)):
    stub = get_vehicles_stub()
    req = vehicles_pb2.CreateVehicleRequest(plate=plate, type=type, brand=brand, model=model, year=year)
    try:
        res = stub.CreateVehicle(req)
        return _vehicle_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehicles", tags=["vehicles"])
@require_valid_token
def list_vehicles(type_filter: Optional[str] = None, status_filter: Optional[str] = None, token_data: TokenData = Depends(validate_token)):
    stub = get_vehicles_stub()
    req = vehicles_pb2.ListVehiclesRequest(type_filter=type_filter or "", status_filter=status_filter or "")
    try:
        res = stub.ListVehicles(req)
        return {"vehicles": [_vehicle_response_to_dict(v) for v in res.vehicles]}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vehicles/{vehicle_id}", tags=["vehicles"])
@require_valid_token
def get_vehicle(vehicle_id: str, token_data: TokenData = Depends(validate_token)):
    stub = get_vehicles_stub()
    req = vehicles_pb2.GetVehicleRequest(id=vehicle_id)
    try:
        res = stub.GetVehicle(req)
        return _vehicle_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/vehicles/{vehicle_id}/status", tags=["vehicles"])
@require_valid_token
def update_vehicle_status(vehicle_id: str, new_status: str, token_data: TokenData = Depends(validate_token)):
    stub = get_vehicles_stub()
    req = vehicles_pb2.UpdateStatusRequest(vehicle_id=vehicle_id, new_status=new_status)
    try:
        res = stub.UpdateVehicleStatus(req)
        return _vehicle_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/vehicles/{vehicle_id}/assign-driver", tags=["vehicles"])
@require_valid_token
def assign_driver(vehicle_id: str, driver_id: str, token_data: TokenData = Depends(validate_token)):
    stub = get_vehicles_stub()
    req = vehicles_pb2.AssignDriverRequest(vehicle_id=vehicle_id, driver_id=driver_id)
    try:
        res = stub.AssignDriver(req)
        return _vehicle_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

def _vehicle_response_to_dict(res):
    return {
        "id": res.id,
        "plate": res.plate,
        "type": res.type,
        "status": res.status,
        "brand": res.brand,
        "model": res.model,
        "year": res.year,
        "assigned_driver": res.assigned_driver if hasattr(res, "assigned_driver") else None
    }

# --- ROUTES ---
@app.post("/routes", tags=["Routes"])
@require_valid_token
def create_route(origin: str = Body(...), destination: str = Body(...), distance: float = Body(...), token_data: TokenData = Depends(validate_token)):
    if token_data.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo Admin puede crear rutas.")
    stub = get_route_stub()
    req = routes_pb2.CreateRouteRequest(origin=origin, destination=destination, distance=distance)
    try:
        res = stub.CreateRoute(req)
        return _route_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/routes/{route_id}", tags=["Routes"])
@require_valid_token
def get_route(route_id: str, token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para consultar rutas.")
    stub = get_route_stub()
    req = routes_pb2.GetRouteRequest(id=route_id)
    try:
        res = stub.GetRoute(req)
        return _route_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/routes", tags=["Routes"])
@require_valid_token
def list_routes(token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para listar rutas.")
    stub = get_route_stub()
    req = routes_pb2.ListRoutesRequest()
    try:
        res = stub.ListRoutes(req)
        return {"routes": [_route_response_to_dict(r) for r in res.routes]}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/routes/{route_id}", tags=["Routes"])
@require_valid_token
def update_route(route_id: str, origin: str = Body(...), destination: str = Body(...), distance: float = Body(...), token_data: TokenData = Depends(validate_token)):
    if token_data.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo Admin puede actualizar rutas.")
    stub = get_route_stub()
    req = routes_pb2.UpdateRouteRequest(id=route_id, origin=origin, destination=destination, distance=distance)
    try:
        res = stub.UpdateRoute(req)
        return _route_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

class AssignVehicleBody(BaseModel):
    vehicle_id: str

@app.put("/routes/{route_id}/assign-vehicle", tags=["Routes"])
@require_valid_token
def assign_route_to_vehicle(route_id: str, body: AssignVehicleBody, token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo Admin y Supervisor pueden asignar vehículos a rutas.")
    stub = get_route_stub()
    req = routes_pb2.AssignRouteToVehicleRequest(route_id=route_id, vehicle_id=body.vehicle_id)
    try:
        res = stub.AssignRouteToVehicle(req)
        return _route_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/routes/{route_id}/fuel-consumption", tags=["Routes"])
@require_valid_token
def calculate_fuel_consumption(route_id: str, token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para consultar consumo de combustible.")
    stub = get_route_stub()
    req = routes_pb2.CalculateFuelConsumptionRequest(route_id=route_id, vehicle_id="")
    try:
        res = stub.CalculateFuelConsumption(req)
        return {"estimated_consumption": res.estimated_consumption, "unit": res.unit}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

def _route_response_to_dict(res):
    return {
        "id": res.id,
        "origin": res.origin,
        "destination": res.destination,
        "distance": res.distance,
        "vehicle_id": res.vehicle_id
    }

# --- FUEL CONSUMPTION ---
@app.post("/fuel", tags=["FuelConsumption"])
@require_valid_token
def register_fuel_consumption(route_id: str = Body(...), vehicle_id: str = Body(...), fuel_amount: float = Body(...), token_data: TokenData = Depends(validate_token)):
    if token_data.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo Admin puede registrar consumo.")
    stub = get_fuel_stub()
    req = fuel_pb2.RegisterFuelConsumptionRequest(route_id=route_id, vehicle_id=vehicle_id, fuel_amount=fuel_amount)
    try:
        res = stub.RegisterFuelConsumption(req)
        return _fuel_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fuel/{consumption_id}", tags=["FuelConsumption"])
@require_valid_token
def get_fuel_consumption(consumption_id: str, token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para consultar consumo.")
    stub = get_fuel_stub()
    req = fuel_pb2.GetFuelConsumptionRequest(id=consumption_id)
    try:
        res = stub.GetFuelConsumption(req)
        return _fuel_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fuel", tags=["FuelConsumption"])
@require_valid_token
def list_fuel_consumptions(route_id: Optional[str] = Query(None), vehicle_id: Optional[str] = Query(None), vehicle_type: Optional[str] = Query(None), token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para listar consumos.")
    stub = get_fuel_stub()
    req = fuel_pb2.ListFuelConsumptionsRequest(route_id=route_id or "", vehicle_id=vehicle_id or "", vehicle_type=vehicle_type or "")
    try:
        res = stub.ListFuelConsumptions(req)
        return {"consumptions": [_fuel_response_to_dict(c) for c in res.consumptions]}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fuel/report/by-vehicle-type", tags=["FuelConsumption"])
@require_valid_token
def report_by_vehicle_type(vehicle_type: str = Query(...), token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para reportes.")
    stub = get_fuel_stub()
    req = fuel_pb2.ReportByVehicleTypeRequest(vehicle_type=vehicle_type)
    try:
        res = stub.ReportByVehicleType(req)
        return {
            "total_fuel": res.total_fuel,
            "count": res.count,
            "consumptions": [_fuel_response_to_dict(c) for c in res.consumptions]
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fuel/compare/{route_id}", tags=["FuelConsumption"])
@require_valid_token
def compare_estimated_vs_real(route_id: str, token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para comparar consumos.")
    stub = get_fuel_stub()
    req = fuel_pb2.CompareEstimatedVsRealRequest(route_id=route_id)
    try:
        res = stub.CompareEstimatedVsReal(req)
        return {
            "estimated": res.estimated,
            "real": res.real,
            "unit": res.unit
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

def _fuel_response_to_dict(res):
    return {
        "id": getattr(res, "id", ""),
        "route_id": getattr(res, "route_id", ""),
        "vehicle_id": getattr(res, "vehicle_id", ""),
        "fuel_amount": getattr(res, "fuel_amount", 0.0),
        "created_at": getattr(res, "created_at", "")
    }

# --- DRIVERS ---
class LicenseTypeEnum(int, Enum):
    Light = 0
    Heavy = 1
    Both = 2

class DriverUpdateBody(BaseModel):
    name: str
    license_type: LicenseTypeEnum
    availability: bool

@app.post("/drivers", tags=["Drivers"])
@require_valid_token
def register_driver(name: str = Body(...), license_type: LicenseTypeEnum = Body(...), availability: bool = Body(...), token_data: TokenData = Depends(validate_token)):
    if token_data.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo Admin puede registrar choferes.")
    stub = get_driver_stub()
    req = drivers_pb2.RegisterDriverRequest(name=name, license_type=license_type, availability=availability)
    try:
        res = stub.RegisterDriver(req)
        return _driver_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drivers/{driver_id}", tags=["Drivers"])
@require_valid_token
def get_driver(driver_id: str, token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para consultar choferes.")
    stub = get_driver_stub()
    req = drivers_pb2.GetDriverRequest(id=driver_id)
    try:
        res = stub.GetDriver(req)
        return _driver_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drivers", tags=["Drivers"])
@require_valid_token
def list_drivers(availability: Optional[bool] = Query(None), license_type: Optional[LicenseTypeEnum] = Query(None), token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Operador', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para listar choferes.")
    stub = get_driver_stub()
    fields = {}
    if availability is not None:
        fields["availability"] = availability
    if license_type is not None:
        fields["license_type"] = license_type
    req = drivers_pb2.ListDriversRequest(**fields)
    try:
        res = stub.ListDrivers(req)
        return {"drivers": [_driver_response_to_dict(d) for d in res.drivers]}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/drivers/{driver_id}", tags=["Drivers"])
@require_valid_token
def update_driver(driver_id: str, body: DriverUpdateBody, token_data: TokenData = Depends(validate_token)):
    if token_data.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo Admin puede actualizar choferes.")
    stub = get_driver_stub()
    req = drivers_pb2.UpdateDriverRequest(id=driver_id, name=body.name, license_type=body.license_type, availability=body.availability)
    try:
        res = stub.UpdateDriver(req)
        return _driver_response_to_dict(res)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

class AssignDriverBody(BaseModel):
    route_id: str
    vehicle_id: str

@app.post("/drivers/{driver_id}/assign", tags=["Drivers"])
@require_valid_token
def assign_driver(driver_id: str, body: AssignDriverBody, token_data: TokenData = Depends(validate_token)):
    if token_data.role not in ['Admin', 'Supervisor']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo Admin y Supervisor pueden asignar choferes.")
    stub = get_driver_stub()
    req = drivers_pb2.AssignDriverRequest(driver_id=driver_id, route_id=body.route_id, vehicle_id=body.vehicle_id)
    try:
        res = stub.AssignDriver(req)
        return {"success": res.success, "message": res.message}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=str(e))

def _driver_response_to_dict(res):
    return {
        "id": getattr(res, "id", ""),
        "name": getattr(res, "name", ""),
        "license_type": getattr(res, "license_type", 0),
        "availability": getattr(res, "availability", False),
        "created_at": getattr(res, "created_at", "")
    }