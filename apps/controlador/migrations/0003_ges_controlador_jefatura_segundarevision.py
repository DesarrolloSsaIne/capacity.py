# Generated by Django 2.2.7 on 2020-04-27 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jefaturas', '0001_initial'),
        ('controlador', '0002_ges_controlador_jefatura_primerarevision'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_controlador',
            name='jefatura_segundarevision',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='jefatura_segundarevision', to='jefaturas.Ges_Jefatura'),
        ),
    ]
