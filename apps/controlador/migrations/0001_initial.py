# Generated by Django 2.2.7 on 2020-03-05 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estado_flujo', '0001_initial'),
        ('jefaturas', '0001_initial'),
        ('periodos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ges_Controlador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel_inicial', models.IntegerField()),
                ('fecha_ultima_modificacion', models.DateField()),
                ('estado_flujo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='estado_flujo.Glo_EstadoFlujo')),
                ('id_jefatura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='jefaturas.Ges_Jefatura')),
                ('id_periodo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='periodos.Glo_Periodos')),
            ],
        ),
    ]
