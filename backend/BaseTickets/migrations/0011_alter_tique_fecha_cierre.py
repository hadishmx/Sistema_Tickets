# Generated by Django 5.1.1 on 2024-10-23 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseTickets', '0010_rename_fecha_tique_fecha_cierre_tique_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tique',
            name='fecha_cierre',
            field=models.DateField(verbose_name='Fecha Tique'),
        ),
    ]