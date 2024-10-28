from django.shortcuts import render
from django.contrib.auth.models import User,Group
from .serializers import UserSerializer,GroupSerializer, UsuarioSerializer,TiqueSerializers
from .models import Usuario,Tique

from rest_framework import permissions, viewsets , status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from django.shortcuts import get_object_or_404

# Create your views here.

from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    print(request.data)
    
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Se requieren nombre de usuario y contraseña."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Obtener el usuario por el nombre de usuario
        user = get_object_or_404(User, username=username)

        # Verificar si la cuenta está activa
        if not user.is_active:
            print("Cuenta inactiva")
            return Response({"error": "La cuenta está inactiva."}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar la contraseña
        if not user.check_password(password):
            return Response({"error": "Contraseña inválida."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener o crear el token
        token, created = Token.objects.get_or_create(user=user)

        # Serializar los datos del usuario
        user_serializer = UserSerializer(instance=user)

        return Response({
            "token": token.key,
            "user": user_serializer.data,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print("Datos recibidos:", request.data)  # Imprimir los datos recibidos

    user_data = {
        'username': request.data.get('username'),
        'email': request.data.get('email'),
        'password': request.data.get('password'),
        
    }

    # Serializar y validar los datos del User
    user_serializer = UserSerializer(data=user_data)

    if user_serializer.is_valid():
        user = user_serializer.save()

        # Crear el modelo Usuario aquí (asegúrate de que los datos se pasen correctamente)
        usuario_data = {
            'user': user.id,  # ID del User
            'rut': request.data.get('rut'),
            'nombre': request.data.get('nombre'),
            'apellido': request.data.get('apellido'),
            'fecha_nacimiento': request.data.get('fecha_nacimiento'),
            'telefono': request.data.get('telefono'),
            'correo': request.data.get('email'),
            'avatar': request.data.get('avatar'),
        }

        usuario_serializer = UsuarioSerializer(data=usuario_data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()

            # Crear el token para el User
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user': user_serializer.data,
                'usuario': usuario_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Serializa los datos para autenticación
        serializer = self.serializer_class(data=request.data, context={'request': request})

        try:
            # Verifica si las credenciales son válidas
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            # Verifica si la cuenta está activa
            if not user.is_active:
                return Response({"error": "La cuenta está inactiva"}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Obtiene o crea el token para el usuario
            token, created = Token.objects.get_or_create(user=user)

            # Devuelve el token y los datos del usuario
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'is_active': user.is_active
            })
        except Exception as e:
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(user=request.user)  # Obtén el usuario autenticado
    except Usuario.DoesNotExist:
        return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_tiques(request):
    # Verifica si el request data es una lista o un solo objeto
    if isinstance(request.data, list):
        # Si es una lista, pasa el argumento many=True al serializador
        serializer = TiqueSerializers(data=request.data, many=True)
    else:
        # Si es un solo objeto, no uses many=True
        serializer = TiqueSerializers(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def group_and_account(request, user_id):
    # Verificar si el usuario autenticado es del grupo "Gerente General"
    if not request.user.groups.filter(name="Director General").exists():
        return Response({"detail": "No tienes permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

    # Obtener el usuario por ID
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Asignar el grupo si se proporciona
    group_name = request.data.get('group_name')
    if group_name:
        try:
            group = Group.objects.get(name=group_name)

            # Remover todos los grupos actuales del usuario
            user.groups.clear()

            # Asignar el nuevo grupo
            user.groups.add(group)
            try:
                usuario_instance = Usuario.objects.get(user=user)
                usuario_instance.tipo = group  # Asignar el grupo al campo 'tipo' de Usuario
                usuario_instance.save()
            except Usuario.DoesNotExist:
                return Response({"detail": "User associated with Usuario not found."}, status=status.HTTP_404_NOT_FOUND)

        except Group.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    # Activar o desactivar la cuenta según el valor proporcionado en la solicitud
    is_active = request.data.get('is_active')
    if is_active is not None:
        user.is_active = is_active
        user.save()

        status_msg = "activated" if is_active else "deactivated"
        return Response({"detail": f"User '{user.username}' has been {status_msg} and group '{group_name}' assigned."}, status=status.HTTP_200_OK)

    return Response({"detail": "Invalid request. 'is_active' field is required."}, status=status.HTTP_400_BAD_REQUEST)









