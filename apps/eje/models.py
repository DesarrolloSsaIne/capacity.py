from django.db import models
from apps.periodos.models import Glo_Periodos
# Create your models here.

class Ges_Ejes (models.Model):
    id_eje = models.CharField(max_length=6, null=True)
    descripcion_eje = models.CharField(max_length=40)
    fecha_creacion = models.DateTimeField(auto_now=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{} | {}'.format(self.id_eje, self.descripcion_eje )
