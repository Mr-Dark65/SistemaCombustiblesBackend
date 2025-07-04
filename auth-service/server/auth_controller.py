import grpc
from generated import auth_pb2
from generated import auth_pb2_grpc
from models import User
from utils import (
    hash_password,
    verify_password,
    generate_jwt,
    verify_jwt
)

class AuthController(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        try:
            # Verificar si el usuario ya existe
            if User.objects(username=request.username).first():
                return auth_pb2.RegisterResponse(
                    success=False,
                    message="El nombre de usuario ya existe"
                )
            
            # Validar rol
            if request.role not in ['Admin', 'Operador', 'Supervisor']:
                return auth_pb2.RegisterResponse(
                    success=False,
                    message="Rol inválido. Los roles válidos son: Admin, Operador, Supervisor"
                )
            
            # Crear nuevo usuario
            hashed_pw = hash_password(request.password)
            user = User(
                username=request.username,
                password=hashed_pw,
                email=request.email,
                role=request.role
            )
            user.save()
            
            return auth_pb2.RegisterResponse(
                success=True,
                message="Usuario registrado exitosamente",
                user_id=str(user.id)
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.RegisterResponse()

    def Login(self, request, context):
        try:
            user = User.objects(username=request.username).first()
            if not user or not verify_password(request.password, user.password):
                return auth_pb2.LoginResponse(
                    success=False,
                    message="Credenciales inválidas"
                )
            
            token = generate_jwt(str(user.id), user.role)
            return auth_pb2.LoginResponse(
                success=True,
                message="Inicio de sesión exitoso",
                token=token,
                role=user.role
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.LoginResponse()

    def ValidateToken(self, request, context):
        try:
            payload = verify_jwt(request.token)
            if not payload:
                return auth_pb2.TokenResponse(valid=False)
            
            # Verificar que el usuario aún existe
            user = User.objects(id=payload.get('sub')).first()
            if not user:
                return auth_pb2.TokenResponse(valid=False)
            
            return auth_pb2.TokenResponse(
                valid=True,
                role=payload.get('role'),
                user_id=payload.get('sub')
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.TokenResponse()