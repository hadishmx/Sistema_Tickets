from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Cliente,Tique,EstadoTique,TipoTique,Criticidad,Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}, 'is_active':{'default': False}}  # La contraseña solo para escritura

    def create(self, validated_data):
        # Verificar si los campos se encuentran en validated_data
        validated_data['is_active'] = False
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        # Si alguno de los campos es None o no existe, lanzar un error de validación
        if not username or not email or not password:
            raise serializers.ValidationError("Todos los campos son obligatorios.")

        # Crear el usuario con los datos validados
        user = User(
            username=username,
            email=email
        )

        # Encriptar la contraseña y guardar el usuario
        user = User(username=username, email=email, is_active=False)
        user.set_password(password)
        user.save()

        return user

        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['user', 'rut', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'correo', 'avatar', 'tipo']

    def create(self, validated_data):
        # Obtener el usuario asociado
        user = validated_data.get('user')
        
        # Crear el modelo Usuario
        usuario = Usuario.objects.create(
            user=user,  # Aquí se relaciona el Usuario con el User
            rut=validated_data.get('rut'),
            nombre=validated_data.get('nombre'),
            apellido=validated_data.get('apellido'),
            fecha_nacimiento=validated_data.get('fecha_nacimiento'),
            telefono=validated_data.get('telefono'),
            correo=validated_data.get('correo'),
            avatar=validated_data.get('avatar'),
            tipo=validated_data.get('tipo'),
        )
        return usuario


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class TiqueSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tique
        fields = '__all__'

class ClienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class EstadoTiqueSerializers(serializers.ModelSerializer):
    class Meta:
        model = EstadoTique
        fields = '__all__'

class TipoTiqueSerializers(serializers.ModelSerializer):
    class Meta:
        model = TipoTique
        fields = '__all__'

class CriticidadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Criticidad
        fields = '__all__'