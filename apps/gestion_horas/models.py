from django.db import models
from apps.estructura.models import Ges_Niveles
from django.contrib.auth.models import User
from apps.jefaturas.models import Ges_Jefatura
from apps.familia_cargo.models import Glo_FamiliaCargo
from apps.periodos.models import Glo_Periodos
from django.utils import timezone as tz
# Create your models here.

class Ges_Registro_Horas(models.Model):
    id_familiacargo = models.ForeignKey(Glo_FamiliaCargo, on_delete=models.PROTECT, null=True)
    id_user = models.ForeignKey(User, on_delete=models.PROTECT )
    id_nivel = models.ForeignKey(Ges_Niveles, on_delete=models.PROTECT)
    tiene_vacaciones = models.BooleanField()
    fecha_inicio = models.DateField(null=True)
    fecha_termino=   models.DateField(null=True)
    dias_habiles = models.IntegerField()
    notas = models.TextField( null=True, blank=True)
    fecha_insercion= models.DateTimeField(auto_now=True, null=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)




