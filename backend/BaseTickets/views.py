from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer,GroupSerializer, UsuarioSerializer,TiqueSerializers
from .models import Usuario,Tique

from rest_framework import permissions, viewsets , status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    print(request.data)

    try:
        # Obtener el usuario por el nombre de usuario
        user = get_object_or_404(User, username=request.data['username'])


        if not user.is_active:
            print("cuenta inactiva")
            return Response({"error": "La cuenta esta inactiva"}, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar la contraseña
        if not user.check_password(request.data['password']):
            return Response({"error": "invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener o crear el token
        token, created = Token.objects.get_or_create(user=user)

        # Serializar los datos del usuario
        user_serializer = UserSerializer(instance=user)
        usuario_serializer = UsuarioSerializer(instance=user.usuario)  # Asegúrate de que el usuario tenga un objeto `Usuario`
        print(int(usuario_serializer.data['user']))
        return Response({
            "token": token.key,
            "user": user_serializer.data,
            #"usuario": usuario_serializer.data,  # Devuelve también los datos del modelo Usuario
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
            'correo': request.data.get('email'),  # Asegúrate de que esto sea correcto
            'avatar': request.data.get('avatar'),
            'login': True,
            'tipo': request.data.get('tipo'),
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

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email  # o cualquier otro dato que quieras retornar
        })
    
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





