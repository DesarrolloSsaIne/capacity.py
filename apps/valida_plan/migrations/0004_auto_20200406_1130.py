# Generated by Django 2.2.7 on 2020-04-06 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('valida_plan', '0003_ges_observaciones_user_observa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ges_observaciones',
            name='user_observa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
