# Generated by Django 5.1.1 on 2024-11-11 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseTickets', '0021_cliente_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha_creacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha registro cliente'),
        ),
    ]