from django.db import models
from apps.periodos.models import Glo_Periodos

# Create your models here.
class Ges_Feriados(models.Model):
    anio_feriado = models.IntegerField()
    fecha_feriado= models.DateField()
    descripcion_feriado= models.CharField(max_length= 150, null=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_feriado)