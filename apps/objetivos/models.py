from django.db import models
from apps.estructura.models import Ges_PrimerNivel, Ges_SegundoNivel, Ges_TercerNivel, Ges_CuartoNivel
from apps.eje.models import Ges_Ejes
from apps.periodos.models import Glo_Periodos
from django.contrib.auth.models import User
# Create your models here.



class Ges_Objetivo_Estrategico (models.Model):
    descripcion_objetivo = models.CharField(max_length=400)
    ges_eje = models.ForeignKey(Ges_Ejes, on_delete=models.PROTECT)
    ges_primer_nivel = models.ForeignKey(Ges_PrimerNivel, on_delete=models.PROTECT)
    fecha_actualizacion= models.DateField(auto_now=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)
    transversal = models.BooleanField(default=False, null=True)
    def __str__(self):
        return '{}'.format(self.descripcion_objetivo)

class Ges_Objetivo_Tactico (models.Model):
    descripcion_objetivo = models.CharField(max_length=400)
    id_segundo_nivel = models.ForeignKey(Ges_SegundoNivel, on_delete=models.PROTECT, null=True, blank=True)
    id_objetivo_estrategico= models.ForeignKey(Ges_Objetivo_Estrategico, on_delete=models.PROTECT, null=True)
    fecha_actualizacion =models.DateField(auto_now=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)
    transversal = models.BooleanField(default=False, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_objetivo)

class Ges_Objetivo_TacticoTN (models.Model):
    descripcion_objetivo = models.CharField(max_length=400)
    id_tercer_nivel = models.ForeignKey(Ges_TercerNivel, on_delete=models.PROTECT, null=True, blank=True)
    id_objetivo_tactico= models.ForeignKey(Ges_Objetivo_Tactico, on_delete=models.PROTECT, null=True)
    fecha_actualizacion =models.DateField(auto_now=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)
    transversal = models.BooleanField(default=False, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_objetivo)


class Ges_Objetivo_Operativo (models.Model):
    descripcion_objetivo = models.CharField(max_length=400)
    id_cuarto_nivel = models.ForeignKey(Ges_CuartoNivel, on_delete=models.PROTECT)
    id_objetivo_tacticotn= models.ForeignKey(Ges_Objetivo_TacticoTN, on_delete=models.PROTECT, null=True)
    fecha_actualizacion =models.DateField(auto_now=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)
    transversal = models.BooleanField(default=False, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_objetivo)