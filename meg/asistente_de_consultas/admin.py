from django.contrib import admin
from .models import *
         
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

class CentroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'id_parr', 'electores')
    list_filter = ['id_parr']
    search_fields = ['id']

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Municipio)
admin.site.register(Parroquia)
admin.site.register(Centro, CentroAdmin)
admin.site.register(Persona)
admin.site.register(HuboCambio)
admin.site.register(CaracteristicasElectorales)
admin.site.register(CaracteristicasSocioeconomicas)
admin.site.register(Origen)
admin.site.register(Email)
admin.site.register(Celular)
admin.site.register(Fijo)
admin.site.register(Empresa)
admin.site.register(Producto)
admin.site.register(Transaccion)
admin.site.register(RefAgregados)
