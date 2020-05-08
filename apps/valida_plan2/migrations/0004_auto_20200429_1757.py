# Generated by Django 2.2.7 on 2020-04-29 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objetivos', '0002_auto_20200319_1225'),
        ('valida_plan2', '0003_auto_20200429_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ges_observaciones_sr',
            name='id_actividad',
        ),
        migrations.RemoveField(
            model_name='ges_observaciones_sr',
            name='id_objetivo',
        ),
        migrations.AddField(
            model_name='ges_observaciones_sr',
            name='id_objetivo_operativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='objetivos.Ges_Objetivo_Operativo'),
        ),
        migrations.AddField(
            model_name='ges_observaciones_sr',
            name='id_objetivo_tactico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='objetivos.Ges_Objetivo_Tactico'),
        ),
        migrations.AddField(
            model_name='ges_observaciones_sr',
            name='id_objetivo_tacticotn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='objetivos.Ges_Objetivo_TacticoTN'),
        ),
    ]
