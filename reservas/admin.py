from django.contrib import admin
from .models import Disiplina, Instalacion, Reserva
# Register your models here.

class DisiplinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado')

class InstalacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'restriciones', 'imagen', 'estado')   #'precio', 'capacidad','indumentaria','recomendaciones', 'equipo_incluido'
    
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'apellidos', 'cedula', 'email', 'telefono', 'fecha_creacion', 'fecha_compra', 'codigo_qr', 'cantidad', 'Presentaciones', 'Productos', 'estado')


admin.site.register(Disiplina, DisiplinaAdmin)
admin.site.register(Instalacion, InstalacionAdmin)
admin.site.register(Reserva, ReservaAdmin)
