# Generated by Django 2.2.7 on 2020-07-27 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('periodos', '0009_glo_validacion'),
        ('estado_actividad', '0003_glo_estadoactividad_orden'),
        ('actividades', '0006_ges_actividad_validada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ges_actividad',
            name='fecha_inicio_actividad',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ges_actividad',
            name='fecha_termino_actividad',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Ges_Observaciones_valida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_observacion', models.CharField(max_length=2000)),
                ('fecha_registro', models.DateTimeField(auto_now=True)),
                ('id_actividad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='actividades.Ges_Actividad')),
                ('id_periodo_valida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='periodos.Glo_validacion')),
            ],
        ),
        migrations.CreateModel(
            name='Ges_log_reportes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now=True)),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('fecha_termino', models.DateTimeField(blank=True, null=True)),
                ('fecha_real_termino', models.DateTimeField(blank=True, null=True)),
                ('id_actividad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='actividades.Ges_Actividad')),
                ('id_estado_actividad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='estado_actividad.Glo_EstadoActividad')),
                ('id_periodo_valida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='periodos.Glo_validacion')),
            ],
        ),
    ]
