# Generated by Django 2.2.7 on 2020-08-25 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_logeventos_metodo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuariosExcepcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
