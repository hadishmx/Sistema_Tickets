# Generated by Django 5.1.1 on 2024-10-25 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseTickets', '0019_alter_tique_usuario_cierra_alter_tique_usuario_crea'),
    ]

    operations = [
        migrations.AddField(
            model_name='tique',
            name='name_cierre',
            field=models.TextField(blank=True, null=True, verbose_name='Ultima modificacion cierre'),
        ),
        migrations.AddField(
            model_name='tique',
            name='name_crea',
            field=models.TextField(blank=True, null=True, verbose_name='Ultima modificacion crea'),
        ),
    ]