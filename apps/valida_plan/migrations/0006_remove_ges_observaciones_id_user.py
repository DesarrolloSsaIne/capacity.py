# Generated by Django 2.2.7 on 2020-04-06 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valida_plan', '0005_auto_20200406_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ges_observaciones',
            name='id_user',
        ),
    ]
