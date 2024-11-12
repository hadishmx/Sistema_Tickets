from .models import Tique,Usuario,Cliente,User,Area
from django.contrib.auth.models import Group
from rest_framework import viewsets,permissions
from .serializers import TiqueSerializers,UsuarioSerializer,ClienteSerializers,UserSerializer,AreaSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,BasePermission
from rest_framework import status
from rest_framework.exceptions import NotFound
from .permissions import IsGerenteGeneralOrReadOnly


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [IsAuthenticated] 
    serializer_class = ClienteSerializers

    def list(self, request, *args, **kwargs):
        # Verificamos a qué grupo pertenece el usuario
        if request.user.groups.filter(name="Ejecutivo").exists():
            # Ejecutivos pueden ver y gestionar todos los tiques
            return super().list(request, *args, **kwargs)
        
        elif request.user.groups.filter(name="Director General").exists():
            # Gerente General tiene acceso total
            return super().list(request, *args, **kwargs)
        
        elif request.user.groups.filter(name="Atencion").exists():
            # Gerente General tiene acceso total
            return super().list(request, *args, **kwargs)
        
        else:
            # Si no pertenece a ningún grupo, denegar el acceso
            return Response({"detail": "No tiene permisos para acceder a esta información."}, status=403)

    def create(self, request, *args, **kwargs):
        # Solo Ejecutivo y Gerente General pueden crear tiques
        if request.user.groups.filter(name="Ejecutivo").exists() or request.user.groups.filter(name="Director General").exists():
            print(request)
            return super().create(request, *args, **kwargs)
        else:
            return Response({"detail": "No tiene permisos para crear clientes."}, status=403)

    def update(self, request, *args, **kwargs):
        # Solo Atención y Gerente General pueden editar tiques
        if request.user.groups.filter(name="Ejecutivo").exists() or request.user.groups.filter(name="Director General").exists() or request.user.groups.filter(name="Atencion").exists():
            return super().update(request, *args, **kwargs)
        else:
            return Response({"detail": "No tiene permisos para editar clientes."}, status=403)


class TiqueViewSet(viewsets.ModelViewSet):
    queryset = Tique.objects.all()
    serializer_class = TiqueSerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Verificamos a qué grupo pertenece el usuario
        if request.user.groups.filter(name="Ejecutivo").exists():
            # Ejecutivos pueden ver y gestionar todos los tiques
            return super().list(request, *args, **kwargs)
        
        elif request.user.groups.filter(name="Atencion").exists():
            # Atención solo puede listar tiques
            queryset = Tique.objects.all()
            serializer = TiqueSerializers(queryset, many=True)
            return Response(serializer.data)
        
        elif request.user.groups.filter(name="Director General").exists():
            # Gerente General tiene acceso total
            return super().list(request, *args, **kwargs)
        
        else:
            # Si no pertenece a ningún grupo, denegar el acceso
            return Response({"detail": "No tiene permisos para acceder a esta información."}, status=403)

    def create(self, request, *args, **kwargs):
        # Solo Ejecutivo y Gerente General pueden crear tiques
        if request.user.groups.filter(name="Ejecutivo").exists() or request.user.groups.filter(name="Director General").exists():
            return super().create(request, *args, **kwargs)
        else:
            return Response({"detail": "No tiene permisos para crear tiques."}, status=403)

    def update(self, request, *args, **kwargs):
        # Solo Atención y Gerente General pueden editar tiques
        if request.user.groups.filter(name="Atencion").exists() or request.user.groups.filter(name="Director General").exists() or request.user.groups.filter(name="Ejecutivo").exists() :
            return super().update(request, *args, **kwargs)
        else:
            return Response({"detail": "No tiene permisos para editar tiques."}, status=403)

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]  
    authentication_classes = [TokenAuthentication] # Requiere Token

    # Filtra para que solo vea su propio registro
    def get_queryset(self):
        # Devuelve solo los datos del usuario autenticado
        return Usuario.objects.filter(user=self.request.user)

    # Opcional: Si deseas permitir que un usuario solo pueda modificar su propia información
    def update(self, request, *args, **kwargs):
    # Obtiene el objeto Usuario correspondiente al usuario autenticado
        try:
            usuario = self.get_queryset().get()  # Esto asegura que solo obtienes el usuario autenticado
        except Usuario.DoesNotExist:
            return Response({"detail": "No Usuario matches the given query."}, status=status.HTTP_404_NOT_FOUND)

        # Verifica que el ID en la URL coincide con el usuario autenticado
        if usuario.user.id != int(kwargs['pk']):
            return Response({"detail": "No tienes permiso para modificar este perfil."}, status=status.HTTP_403_FORBIDDEN)

        # Continúa con la actualización
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Sobrescribe el método retrieve si necesitas personalizar la respuesta
    def retrieve(self, request, *args, **kwargs):
    # Intenta obtener el usuario autenticado
        try:
            usuario = self.get_queryset().get()  # Solo obtiene el usuario autenticado
        except Usuario.DoesNotExist:
            return Response({"detail": "No Usuario matches the given query."}, status=status.HTTP_404_NOT_FOUND)

        # Verifica que el ID en la URL coincide con el usuario autenticado
        if usuario.user.id != kwargs['pk']:
            return Response({"detail": "No tienes permiso para ver este perfil."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(usuario)
        return Response(serializer.data) 
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated | IsAdminUser] 
    serializer_class = UserSerializer

    def get_queryset(self):
        # Intentar obtener el grupo 'Gerente General'
        try:
            gerente_general_group = Group.objects.get(name="Director General")
        except Group.DoesNotExist:
            return User.objects.filter(id=self.request.user.id)

        # Si el usuario está en el grupo 'Gerente General', puede ver todas las cuentas
        if gerente_general_group in self.request.user.groups.all():
            return User.objects.all()
        
        # Para los demás, devolver solo su propia cuenta
        return User.objects.filter(id=self.request.user.id)
    




