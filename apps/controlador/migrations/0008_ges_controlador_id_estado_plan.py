# Generated by Django 2.2.7 on 2020-05-26 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estado_plan', '0002_remove_glo_estadoplan_estado'),
        ('controlador', '0007_ges_controlador_analista_asignado'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_controlador',
            name='id_estado_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='estado_plan.Glo_EstadoPlan'),
        ),
    ]
