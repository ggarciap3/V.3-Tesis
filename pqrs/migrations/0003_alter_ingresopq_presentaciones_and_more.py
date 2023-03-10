# Generated by Django 4.1.5 on 2023-03-11 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrs', '0002_alter_ingresopq_presentaciones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingresopq',
            name='Presentaciones',
            field=models.IntegerField(choices=[[1, '500g'], [2, '1kg'], [3, '2kg'], [4, '5kg'], [5, '10kg'], [6, '25kg'], [7, '50kg'], [8, 'Stick Packs']]),
        ),
        migrations.AlterField(
            model_name='ingresopq',
            name='Productos',
            field=models.IntegerField(choices=[(1, 'Azucar Blanca'), (2, 'Azucar Morena'), (3, 'Azucar Ligero'), (4, 'Azucar Turbinado'), (5, 'Azucar Blanco Organico'), (6, 'Azucar De Coco Organico'), (7, 'Panela'), (8, 'Steviazucar Blanca'), (9, 'Steviazucar Morena'), (10, 'Stevia Panela')]),
        ),
        migrations.AlterField(
            model_name='ingresopq',
            name='evidencia',
            field=models.ImageField(upload_to='imagenes/ingresopqs/%Y/%m/%d/'),
        ),
    ]
