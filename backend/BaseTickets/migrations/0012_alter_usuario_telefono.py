# Generated by Django 5.1.1 on 2024-10-24 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseTickets', '0011_alter_tique_fecha_cierre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Teléfono Usuario'),
        ),
    ]
