# Generated by Django 2.2.7 on 2021-03-24 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0015_ges_actividad_flag_fri'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ges_actividad',
            name='flag_fri',
        ),
    ]
