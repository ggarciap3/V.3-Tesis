# Generated by Django 4.1.5 on 2023-03-04 11:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoriapq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10, unique=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Categoriapq',
                'verbose_name_plural': 'PQRS_Categorias',
            },
        ),
        migrations.CreateModel(
            name='Tipospq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('restriciones', models.CharField(max_length=200)),
                ('imagen', models.ImageField(upload_to='imagenes/tipospqs/%Y/%m/%d/')),
                ('estado', models.BooleanField(default=True)),
                ('id_categoriap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pqrs.categoriapq')),
            ],
            options={
                'verbose_name': 'Tipospq',
                'verbose_name_plural': 'PQRS_TiposPQ',
            },
        ),
        migrations.CreateModel(
            name='Ingresopq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('cedula', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=10)),
                ('fecha_creacion', models.DateField(default=datetime.datetime.now)),
                ('fecha_compra', models.DateField()),
                ('num_factura', models.CharField(max_length=15)),
                ('descrip', models.CharField(max_length=400)),
                ('cantidad', models.CharField(max_length=10)),
                ('Presentaciones', models.IntegerField(choices=[[0, '..........'], [1, '500g'], [2, '1kg'], [3, '2kg'], [4, '5kg'], [5, '10kg'], [6, '25kg'], [7, '50kg'], [8, 'Stick Packs']])),
                ('Productos', models.IntegerField(choices=[(0, '..........'), (1, 'Azucar Blanca'), (2, 'Azucar Morena'), (3, 'Azucar Ligero'), (4, 'Azucar Turbinado'), (5, 'Azucar Blanco Organico'), (6, 'Azucar De Coco Organico'), (7, 'Panela'), (8, 'Steviazucar Blanca'), (9, 'Steviazucar Morena'), (10, 'Stevia Panela')])),
                ('evidencia', models.CharField(max_length=400)),
                ('estado', models.BooleanField(default=True)),
                ('id_tipospq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pqrs.tipospq')),
            ],
            options={
                'verbose_name': 'Ingresopq',
                'verbose_name_plural': 'PQRS_Quejas&Reclamos',
            },
        ),
    ]
