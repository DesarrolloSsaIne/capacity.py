# Generated by Django 2.2.7 on 2020-07-30 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0008_ges_log_reportes_id_periodo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ges_log_reportes',
            old_name='fecha_inicio',
            new_name='fecha_reprogramacion_inicio',
        ),
        migrations.RenameField(
            model_name='ges_log_reportes',
            old_name='fecha_termino',
            new_name='fecha_reprogramacion_termino',
        ),
        migrations.AddField(
            model_name='ges_log_reportes',
            name='justificacion',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]