# Generated by Django 5.1.1 on 2024-12-15 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseTickets', '0003_remove_criticidad_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='tique',
            name='fecha_pago',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]