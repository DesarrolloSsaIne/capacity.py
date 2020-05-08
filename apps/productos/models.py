from django.db import models
from apps.periodos.models import Glo_Periodos
# Create your models here.
class Glo_ProductosEstadisticos(models.Model):
    descripcion_producto = models.CharField(max_length=200)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{} '.format( self.descripcion_producto)