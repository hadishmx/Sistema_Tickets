# Generated by Django 5.1.1 on 2024-10-25 21:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseTickets', '0017_alter_tique_usuario_cierra_alter_tique_usuario_crea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tique',
            name='usuario_cierra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_usuario_cierra', to='BaseTickets.usuario', verbose_name='Usuario Cierra'),
        ),
        migrations.AlterField(
            model_name='tique',
            name='usuario_crea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_usuario_crea', to='BaseTickets.usuario', verbose_name='Usuario Crea'),
        ),
    ]
