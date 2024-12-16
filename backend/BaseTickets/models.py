from django.db import models
from django.db import models
from django.contrib.auth.models import User,Group
import uuid
import os

# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=10, verbose_name="Rut Usuario")
    nombre = models.CharField(max_length=50, verbose_name="Nombre Usuario")
    apellido = models.CharField(max_length=50, verbose_name="Apellido Usuario")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento Usuario", null=True)
    telefono = models.CharField(verbose_name="Teléfono Usuario", null=True, blank=True, max_length=9)
    correo = models.EmailField(verbose_name="Correo Electrónico Usuario")
    avatar = models.ImageField(verbose_name="Avatar Usuario", upload_to="profile", null=True, blank=True)
    tipo = models.ForeignKey(Group, verbose_name="Tipo de Usuario", on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si ya existe una imagen y es diferente de la nueva, elimina la anterior
        if self.pk:
            old_avatar = Usuario.objects.filter(pk=self.pk).first().avatar
            if old_avatar and old_avatar != self.avatar:
                if os.path.isfile(old_avatar.path):  # Asegúrate de que el archivo existe
                    os.remove(old_avatar.path)  # Elimina el archivo

        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.nombre + " " + self.apellido

#------------------------------------------------------------No se utilizan los de arriba -----------------------------------

class Criticidad(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='ID criticidad' )
    nombre = models.CharField(max_length=50, verbose_name="Nombre Criticidad")

    def __str__(self) -> str:
        return self.nombre

class Cliente(models.Model):
    rut = models.CharField(primary_key=True, max_length=10, verbose_name="Rut Cliente")
    nombre = models.CharField(max_length=50, verbose_name="Nombre Cliente")
    apellido = models.CharField(max_length=50, verbose_name="Apellido Cliente")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento Cliente", null=True)
    telefono = models.CharField(verbose_name="Teléfono Cliente", max_length=9)
    correo = models.EmailField(verbose_name="Correo Electrónico Cliente")
    avatar = models.ImageField(verbose_name="Avatar Cliente", upload_to="profile", null=True, blank=True)
    fecha_creacion = models.DateField(verbose_name="Fecha registro cliente",null=True, blank=True)

    def __str__(self) -> str:
        return self.nombre + " " + self.apellido

class EstadoTique(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='ID Estado Tique' )
    nombre = models.CharField(max_length=50, verbose_name="Nombre EstadoTique")

    def __str__(self) -> str:
        return self.nombre

class TipoTique(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='ID tipo tique' )
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre TipoTique")

    def __str__(self):
        return self.nombre
    
class Area(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='ID Area' )
    nombre = models.CharField(max_length=50, verbose_name="Nombre Area")
    
    def __str__(self) -> str:
        return self.nombre
        

class Tique(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name='ID tique')
    fecha_creacion = models.DateField(auto_now_add=True,verbose_name="Fecha creacion")
    problema = models.TextField(verbose_name="Detalle Problema")
    servicio = models.TextField(verbose_name="Detalle Servicio")
    observacion = models.TextField(verbose_name="Observación", null=True, blank=True)
    cliente = models.ForeignKey(Cliente, verbose_name="Rut Cliente", on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name="Área",on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoTique, verbose_name="Tipo", on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoTique, verbose_name="Estado", on_delete=models.CASCADE, null=True, blank=True)
    criticidad = models.ForeignKey(Criticidad, verbose_name="Estado", on_delete=models.CASCADE)
    costo = models.DecimalField(verbose_name="Precio trabajo",max_digits=10, decimal_places=2 ,null=True, blank=True)
    estadopago = models.BooleanField(verbose_name="Estado pago", null=True, blank=True, default=False)
    fecha_cierre = models.DateField(verbose_name="Fecha cierre",null=True, blank=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    usuario_crea = models.ForeignKey(User, verbose_name="Usuario Crea", on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_usuario_crea')
    usuario_cierra = models.ForeignKey(User, verbose_name="Usuario Cierra", on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_usuario_cierra')
    name_crea = models.TextField(verbose_name="Ultima modificacion crea",null=True,blank=True)
    name_cierre = models.TextField(verbose_name="Ultima modificacion cierre",null=True,blank=True)

    class Meta:
        db_table = 'tique'

    def __str__(self) -> str:
        return self.problema
    
