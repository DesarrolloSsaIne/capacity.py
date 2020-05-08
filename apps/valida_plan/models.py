from django.db import models
from apps.jefaturas.models import Ges_Jefatura
from apps.periodos.models import Glo_Periodos
from apps.actividades.models import Ges_Actividad
from apps.controlador.models import Ges_Controlador
from django.contrib.auth.models import User
from django.utils import timezone as tz
from apps.objetivos.models import Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN, Ges_Objetivo_Operativo

# Create your models here.

class Ges_Observaciones(models.Model):
    user_observa= models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    id_jefe_observa= models.ForeignKey(Ges_Controlador, on_delete=models.PROTECT, blank=True, null=True)
    id_actividad = models.ForeignKey(Ges_Actividad, on_delete=models.PROTECT, blank=True, null=True)
    observacion = models.CharField(max_length=3000, blank=True, null=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, blank=True, null=True)
    id_controlador= models.IntegerField(null=True) #campo agregado por JR - sprint 8 - Ok
    id_objetivo= models.IntegerField(null=True) #campo agregado por JR- sprint 8 - Ok
    fecha_registro = models.DateTimeField(default=tz.now) #campo modificado por JR- sprint 8 - Ok
    observado= models.IntegerField(blank=True, null=True)

