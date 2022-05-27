# Generated by Django 2.2.7 on 2022-03-22 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jefaturas', '0001_initial'),

        ('controlador', '0011_auto_20201117_1043'),
        ('actividades', '0014_auto_20211203_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_observaciones_valida',
            name='id_controlador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='controlador.Ges_Controlador'),
        ),
        migrations.AddField(
            model_name='ges_observaciones_valida',
            name='id_periodo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='periodos.Glo_Periodos'),
        ),
        migrations.AddField(
            model_name='ges_observaciones_valida',
            name='jefatura_primerarevision',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='jefaturas.Ges_Jefatura'),
        ),
    ]