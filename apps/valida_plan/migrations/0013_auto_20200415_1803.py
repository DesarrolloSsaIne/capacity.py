# Generated by Django 2.2.7 on 2020-04-15 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valida_plan', '0012_auto_20200414_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_observaciones',
            name='id_controlador',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ges_observaciones',
            name='id_objetivo',
            field=models.IntegerField(null=True),
        ),
    ]
