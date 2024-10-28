from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Cliente,Tique,EstadoTique,TipoTique,Criticidad,Usuario,AreaTique

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    grupos = GroupSerializer(many=True, source='groups',required=False)
    

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active','grupos']
        extra_kwargs = {'password': {'write_only': True}, 'is_active':{'default': False}}  # La contraseña solo para escritura

    def create(self, validated_data):
        # Verificar si los campos se encuentran en validated_data
        validated_data['is_active'] = False
        username = validated_data.get('username')
        grupos= validated_data.get('groups',None)
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

        if not grupos:
            default_group, _ = Group.objects.get_or_create(name="Sin Asignar")
            user.groups.add(default_group)
        else:
            # Si se envía grupo, asignarlo
            for grupos in grupos:
                group = Group.objects.get(name=grupos['name'])
                user.groups.add(group)


        return user
    
    def update(self, instance, validated_data):
        # Prevenir que usuarios fuera del grupo 'Gerente General' modifiquen 'is_active'
        request = self.context['request']
        gerente_general_group = Group.objects.get(name="Director General")
        
        if gerente_general_group not in request.user.groups.all():
            validated_data.pop('is_active', None)
        
        return super().update(instance, validated_data)

        
class UsuarioSerializer(serializers.ModelSerializer):
    grupos = GroupSerializer(source='tipo', required=False)  # Usa 'tipo' como fuente para el grupo asociado
    fecha_nacimiento = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Usuario
        fields = ['user', 'rut', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'correo', 'avatar', 'grupos']

    def create(self, validated_data):
        # Obtener el usuario asociado
        user = validated_data.pop('user')  # Extrae el usuario
        
        # Si no se incluye 'tipo' (grupo) en validated_data, se establece como None
        tipo = validated_data.pop('tipo', None)
        
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
            tipo=tipo  # Relaciona el tipo de grupo
        )
        return usuario



class TiqueSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tique
        fields = '__all__'  # O especifica los campos que necesites

class ClienteSerializers(serializers.ModelSerializer):
    fecha_nacimiento = serializers.DateField(format='%d-%m-%Y')

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

class AreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = AreaTique
        fields = '__all__'