from django.contrib import admin
from .models import Categoriapq, Tipospq, Ingresopq
# Register your models here.

class CategoriapqAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado')

class TipospqAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'restriciones', 'imagen', 'estado')   #'precio', 'capacidad','indumentaria','recomendaciones', 'equipo_incluido'
    
class IngresopqAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'apellidos', 'cedula', 'email', 'telefono', 'fecha_creacion', 'fecha_compra','num_factura','cantidad','descrip', 'Presentaciones', 'Productos','evidencia', 'estado') #'codigo_qr'


admin.site.register(Categoriapq, CategoriapqAdmin)
admin.site.register(Tipospq, TipospqAdmin)
admin.site.register(Ingresopq, IngresopqAdmin)
