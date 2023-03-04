from django.db import models
from datetime import datetime #tiempo

# Create your models here.

class Categoriapq(models.Model):
    nombre = models.CharField(max_length=10, unique=True)
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "PQRS_Categorias"
        verbose_name = ("Categoriapq")

    def __str__(self):
        return self.nombre

# Datos De La Nueva Instalacion
class Tipospq(models.Model):
    id_categoriap = models.ForeignKey(Categoriapq, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.CharField(max_length=200)
    restriciones = models.CharField(max_length=200)
    # precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    #capacidad = models.CharField(max_length=10)
    imagen = models.ImageField(upload_to='imagenes/tipospqs/%Y/%m/%d/')
    #indumentaria = models.CharField(max_length=200)
    #recomendaciones = models.CharField(max_length=200)
    #equipo_incluido = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "PQRS_TiposPQ"
        verbose_name = ("Tipospq")
    def __str__(self):
        return self.nombre

# opciones_horaInicio
opciones_Presentaciones = [
    [0,'500g'],
    [1,'1kg'],
    [2,'2kg'],
    [3,'5kg'],
    [4,'10kg'],
    [5,'25kg'],
    [6,'50kg'],
    [7,'Stick Packs'],
]
# opciones_horaFin
opciones_Productos = [
    (0,'Azucar Blanca'),
    (1,'Azucar Morena'),
    (2,'Azucar Ligero'),
    (3,'Azucar Turbinado'),
    (4,'Azucar Blanco Organico'),
    (5,'Azucar De Coco Organico'),
    (6,'Panela'),
    (7,'Steviazucar Blanca'),
    (8,'Steviazucar Morena'),
    (9,'Stevia Panela'),

]



class Ingresopq(models.Model):
    id_tipospq = models.ForeignKey(Tipospq, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    cedula = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    fecha_creacion = models.DateField(default=datetime.now)
    fecha_compra = models.DateField()
    # codigo_qr = models.CharField(max_length=255, unique=True)
    num_factura = models.CharField(max_length=15)
    descrip = models.CharField(max_length=400)
    cantidad = models.CharField(max_length=10)
    Presentaciones = models.IntegerField(choices=opciones_Presentaciones)
    Productos = models.IntegerField(choices=opciones_Productos) 
    evidencia = models.CharField(max_length=400)
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "PQRS_Quejas&Reclamos"
        verbose_name = ("Ingresopq")