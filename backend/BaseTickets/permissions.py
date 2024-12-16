from rest_framework.permissions import BasePermission
from rest_framework import permissions
from django.contrib.auth.models import Group

class IsGerenteGeneralOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir métodos seguros (GET, HEAD, OPTIONS) para todos los usuarios autenticados
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Verificar si el usuario pertenece al grupo 'Gerente General'
        gerente_general_group = Group.objects.get(name="Gerente General")
        if gerente_general_group in request.user.groups.all():
            return True
        
        # Si no está en el grupo, no tiene permiso para modificar datos
        return False

    def has_object_permission(self, request, view, obj):
        # Permitir que los usuarios vean solo su propia información (GET)
        if request.method in permissions.SAFE_METHODS:
            return obj == request.user
        
        # Permitir cambios solo si el usuario está en 'Gerente General'
        gerente_general_group = Group.objects.get(name="Gerente General")
        return gerente_general_group in request.user.groups.all()
    

class IsEjecutivo(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        ejecutivo_group = Group.objects.get(name="Ejecutivo Cliente")
        if ejecutivo_group in request.user.groups.all():
            return True
        
        return False
    
class IsAtencion(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        atencion_group = Group.objects.get(name="Ejecutivo Tecnico")
        if atencion_group in request.user.groups.all():
            return True
        
        return False
