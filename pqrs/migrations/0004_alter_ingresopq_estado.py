# Generated by Django 4.1.5 on 2023-03-12 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrs', '0003_alter_ingresopq_presentaciones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingresopq',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
