from django.db import models

from apps.estado_seguimiento.models import Glo_EstadoSeguimiento
# Create your models here.

class Glo_Periodos_Seguimiento(models.Model):
    id_periodo= models.IntegerField(blank=True, null=True)
    fecha_inicio= models.DateField(blank=True, null=True)
    fecha_termino= models.DateField(blank=True, null=True)
    id_estado_seguimiento= models.ForeignKey(Glo_EstadoSeguimiento, on_delete=models.PROTECT, null=True, blank=True)
