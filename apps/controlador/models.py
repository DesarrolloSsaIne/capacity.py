from django.db import models
from apps.periodos.models import Glo_Periodos
from apps.estado_flujo.models import Glo_EstadoFlujo
from apps.jefaturas.models import Ges_Jefatura
from apps.estructura.models import Ges_Niveles
from django.utils import timezone as tz
from django.contrib.auth.models import User
from apps.estado_plan.models import Glo_EstadoPlan
# Create your models here.

class Ges_Controlador(models.Model):
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT)
    id_jefatura= models.ForeignKey(Ges_Jefatura, on_delete=models.PROTECT, null=True)
    nivel_inicial= models.IntegerField()
    estado_flujo = models.ForeignKey(Glo_EstadoFlujo, on_delete=models.PROTECT)
    fecha_ultima_modificacion= models.DateField(auto_now=True)
    jefatura_primerarevision = models.ForeignKey(Ges_Jefatura, on_delete=models.PROTECT, null=True,
                                                 related_name="jefatura_primerarevision")
    jefatura_segundarevision = models.ForeignKey(Ges_Jefatura, on_delete=models.PROTECT, null=True,
                                                 related_name="jefatura_segundarevision")
    analista_asignado  = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    id_estado_plan = models.ForeignKey(Glo_EstadoPlan, on_delete=models.PROTECT, null=True, blank=True)


