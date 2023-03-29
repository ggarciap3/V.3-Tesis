from django.contrib import admin
from .models import Categoriapq, Tipospq, Ingresopq
# Register your models here.

class CategoriapqAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado')

class TipospqAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'imagen', 'estado')#'restriciones',
    
class IngresopqAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'apellidos', 'cedula', 'email', 'telefono', 'fecha_creacion', 'fecha_compra','lote','cantidad','descrip', 'Presentaciones', 'Productos','evidencia', 'estado','doc', 'estadodoc') 


admin.site.register(Categoriapq, CategoriapqAdmin)
admin.site.register(Tipospq, TipospqAdmin)
admin.site.register(Ingresopq, IngresopqAdmin)

