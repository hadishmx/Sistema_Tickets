from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Cliente,Tique,EstadoTique,TipoTique,Criticidad,Usuario,Area

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
        gerente_general_group = Group.objects.get(name="Gerente General")
        
        if gerente_general_group not in request.user.groups.all():
            validated_data.pop('is_active', None)
        
        return super().update(instance, validated_data)


        
class UsuarioSerializer(serializers.ModelSerializer):
    grupos = GroupSerializer(source='tipo', required=False)  # Usa 'tipo' como fuente para el grupo asociado
    fecha_nacimiento = serializers.DateField(format='%d-%m-%Y')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Sigue aceptando el ID del User
    
    class Meta:
        model = Usuario
        fields = ['user', 'rut', 'nombre', 'apellido', 'fecha_nacimiento', 'telefono', 'correo', 'avatar', 'grupos']

    def create(self, validated_data):
        user = validated_data.pop('user')  # Extrae el objeto User
        usuario = Usuario.objects.create(user=user, **validated_data)
        return usuario




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
        model = Area
        fields = '__all__'

class TiqueSerializers(serializers.ModelSerializer):
    tipo = serializers.SlugRelatedField(
        queryset=TipoTique.objects.all(),
        slug_field='nombre')  # Permite identificar el TipoTique por su nombre
    
    area = serializers.SlugRelatedField(
        queryset=Area.objects.all(),
        slug_field='nombre')
    
    criticidad = serializers.SlugRelatedField(
        queryset=Criticidad.objects.all(),
        slug_field='nombre')
    
    estado = serializers.SlugRelatedField(
        queryset=EstadoTique.objects.all(),
        slug_field='nombre')
    

    rut_cliente = serializers.CharField(source='cliente.rut', read_only=True)
    class Meta:
        model = Tique
        fields = '__all__'  # O especifica los campos que necesites

    def create(self, validated_data):
        tipo_nombre = validated_data['tipo']
        tipo = TipoTique.objects.get(nombre=tipo_nombre)  # Buscar el tipo por su nombre
        validated_data['tipo'] = tipo  # Asignamos el objeto 'TipoTique' en lugar del nombre
        return super().create(validated_data)

class ContactFormSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    TituloAsunto = serializers.CharField(max_length=100)
    telefono = serializers.CharField(max_length=9)
    mensaje = serializers.CharField(max_length=500)