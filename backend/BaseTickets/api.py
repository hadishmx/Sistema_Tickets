from .models import Tique,Usuario,Cliente,User
from rest_framework import viewsets,permissions
from .serializers import TiqueSerializers,UsuarioSerializer,ClienteSerializers,UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [IsAuthenticated] 
    serializer_class = ClienteSerializers


class TiqueViewSet(viewsets.ModelViewSet):
    queryset = Tique.objects.all()
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados pueden acceder
    serializer_class = TiqueSerializers

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

    # Sobrescribe el método `retrieve` si necesitas personalizar la respuesta
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
    permission_classes = [IsAuthenticated] 
    serializer_class = UserSerializer
    


