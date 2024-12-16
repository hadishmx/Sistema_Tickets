
from .serializers import UserSerializer,GroupSerializer, UsuarioSerializer,TiqueSerializers,ContactFormSerializer
from .models import Usuario,Tique
from .permissions import IsGerenteGeneralOrReadOnly

from rest_framework import permissions, viewsets , status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView

from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import requests

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType


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
        usuario = user.usuario

        return Response({
            "token": token.key,
            "user": user_serializer.data,
            "Nombre":usuario.nombre,
            "Apellido":usuario.apellido,

        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer, UsuarioSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print("Datos recibidos:", request.data)  # Imprimir los datos recibidos

    # Extraer los datos para crear un User
    user_data = {
        'username': request.data.get('username'),
        'email': request.data.get('email'),
        'password': request.data.get('password'),
    }

    # Serializar y validar los datos del User
    user_serializer = UserSerializer(data=user_data)

    if user_serializer.is_valid():
        # Crear el objeto User
        user = user_serializer.save()

        # Crear los datos del Usuario con el User creado
        usuario_data = {
            'user': user.id,  # Usar el objeto user directamente
            'rut': request.data.get('rut'),
            'nombre': request.data.get('nombre'),
            'apellido': request.data.get('apellido'),
            'fecha_nacimiento': request.data.get('fecha_nacimiento'),
            'telefono': request.data.get('telefono'),
            'correo': request.data.get('email'),
            'avatar': request.data.get('avatar'),
        }

        # Serializar y validar los datos del Usuario
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        if usuario_serializer.is_valid():
            # Guardar el Usuario
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
    if not request.user.groups.filter(name="Gerente General").exists():
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

class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['nombre']
            email = serializer.validated_data['email']
            mensaje = serializer.validated_data['mensaje']
            telefono = serializer.validated_data['telefono']
            TituloAsunto = serializer.validated_data['TituloAsunto']

            # Componer el correo
            asunto = f"Nuevo mensaje de contacto de {nombre}, con su numero {telefono} con el asunto {TituloAsunto}"
            mensaje_correo = f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"
            destinatario = 'bravohadish@gmail.com'  # Reemplaza con el correo del jefe

            try:
                send_mail(asunto, mensaje_correo, email, [destinatario])
                return Response({'message': 'Correo enviado exitosamente'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TransbankTransactionAPIView(APIView):
    def post(self, request,*args, **kwargs):

        data = request.POST
        tique_id = request.data.get("id")

        if not tique_id:
            return JsonResponse({"error": "El ID del tique no fue proporcionado."}, status=400)
        
        tique = get_object_or_404(Tique, id=tique_id)
        # URL de Transbank para el entorno de pruebas
        url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
        
        # Credenciales de Transbank (reemplázalas con las tuyas)
        headers = {
            "Tbk-Api-Key-Id": "597055555532",  # API Key ID (código comercio)
            "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",  # API Key Secret
            "Content-Type": "application/json"
        }
        
        # Datos necesarios para la transacción
        data = {
            "buy_order": f"{tique.id}",  # Número único para identificar la orden
            "session_id": f"{tique.id}",  # ID de sesión
            "amount": float(tique.costo),  # Monto de la transacción
            "return_url": "http://localhost:8000/recibir-pago/"  # URL de retorno
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Lanza una excepción si la respuesta HTTP es un error
            
            # Imprimir los detalles de la respuesta para depuración
            print("Respuesta de Transbank:", response.json())  # Asegúrate de imprimir el contenido de la respuesta
            
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error al realizar la solicitud:", e)  # Imprime cualquier excepción de la solicitud
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging
from django.utils import timezone
logger = logging.getLogger(__name__)

@api_view(['POST', 'GET'])
def recibir_pago(request):
    if request.method == 'POST':
        # Este bloque maneja la solicitud POST, que es cuando Transbank envía los datos para procesar el pago
        try:
            # Extraer los datos enviados por Transbank
            tique_id = request.data.get('tique_id')  # ID del tique en tu sistema
            estado_pago = request.data.get('estado_pago')  # True o False
            monto = request.data.get('monto')  # Monto aprobado por Transbank
            if not tique_id or estado_pago is None or monto is None:
                return Response({"detail": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)

            # Buscar el tique en la base de datos
            tique = Tique.objects.filter(id=tique_id).first()
            if not tique:
                return Response({"detail": "Tique no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Actualizar el estado del pago
            tique.estado_pago = estado_pago
            tique.monto = monto  # Actualizar el monto con lo recibido de Transbank
            if estado_pago:
                tique.fecha_pago = timezone.now()  # Establecer la fecha de pago si está aprobado
            tique.save()

            # Responder a Transbank con un OK
            return Response({"detail": "Pago procesado correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error al procesar el pago: {str(e)}")
            return Response({"detail": "Error interno al procesar el pago"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'GET':
        # Este bloque maneja la solicitud GET, que es cuando Transbank redirige con el estado de la transacción
        try:
            logger.debug(f"Parámetros GET recibidos: {request.GET}")
            # Obtener los parámetros enviados por Transbank
            tbk_token = request.GET.get("TBK_TOKEN")
            tbk_orden_compra = request.GET.get("TBK_ORDEN_COMPRA")
            tbk_id_sesion = request.GET.get("TBK_ID_SESION")

            if not tbk_token or not tbk_orden_compra:
                return Response({"detail": "Faltan parámetros importantes."}, status=status.HTTP_400_BAD_REQUEST)

            # Llamar a Transbank para obtener el estado de la transacción
            url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{tbk_orden_compra}"
            headers = {
                "Tbk-Api-Key-Id": "XXX",  # Tu API Key ID
                "Tbk-Api-Key-Secret": "XXX",  # Tu API Key Secret
                "Content-Type": "application/json"
            }

            # Realizar la consulta de estado de la transacción
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Obtener los detalles de la respuesta
            result = response.json()

            if result.get('status') == 'AUTHORIZED':
                # Procesar el pago como aprobado
                tique = get_object_or_404(Tique, id=tbk_orden_compra)
                tique.estado_pago = True  # Marcar como pagado
                tique.fecha_pago = timezone.now()  # Fecha del pago
                tique.save()

                return Response({"detail": "Pago aprobado, transacción exitosa."}, status=status.HTTP_200_OK)

            elif result.get('status') == 'REJECTED':
                # Procesar el pago como rechazado
                tique = get_object_or_404(Tique, id=tbk_orden_compra)
                tique.estado_pago = False  # Marcar como rechazado
                tique.save()

                return Response({"detail": "Pago rechazado."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Estado de pago no válido."}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error al procesar la consulta de estado: {str(e)}")
            return Response({"detail": "Error al contactar con Transbank."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_usuarios(request):
    # Verificar si el usuario pertenece al grupo "Gerente General"
    if not request.user.groups.filter(name="Gerente General").exists():
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Recuperar todos los usuarios y sus datos relacionados
    usuarios = Usuario.objects.all()
    response_data = []

    for usuario in usuarios:
        usuario_serializer = UsuarioSerializer(usuario)
        user_serializer = UserSerializer(usuario.user)

        # Combinar los datos de Usuario y User
        combined_data = {
            "usuario": usuario_serializer.data,
            "user": user_serializer.data,
        }
        response_data.append(combined_data)

    return Response(response_data, status=status.HTTP_200_OK)


        
    














