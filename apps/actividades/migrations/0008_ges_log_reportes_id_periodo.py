# Generated by Django 2.2.7 on 2020-07-30 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('periodos', '0009_glo_validacion'),
        ('actividades', '0007_auto_20200727_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='ges_log_reportes',
            name='id_periodo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='periodos.Glo_Periodos'),
        ),
    ]
