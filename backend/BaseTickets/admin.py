from django.contrib import admin
from .models import Criticidad, Cliente, EstadoTique,TipoTique,Tique,Usuario
# Register your models here.

class FichaAdmin(admin.ModelAdmin):
    readonly_fields: ('id')

admin.site.register(Usuario)
admin.site.register(Criticidad)
admin.site.register(Cliente)
admin.site.register(EstadoTique)
admin.site.register(TipoTique)
admin.site.register(Tique)
