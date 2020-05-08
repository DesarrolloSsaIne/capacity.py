from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import User
from apps.periodos.models import Glo_Periodos
from django import forms
from django.contrib.auth import get_user_model
# Create your models here.
#User = get_user_model()

class Ges_PrimerNivel(models.Model):

    descripcion_nivel = models.CharField(max_length=80)
    estado = models.BooleanField()
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_nivel)

class Ges_SegundoNivel(models.Model):

    descripcion_nivel = models.CharField(max_length=80)
    primer_nivel = models.ForeignKey(Ges_PrimerNivel, on_delete=models.PROTECT)
    estado = models.BooleanField()
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_nivel)

class Ges_TercerNivel(models.Model):

    descripcion_nivel = models.CharField(max_length=80)
    segundo_nivel = models.ForeignKey(Ges_SegundoNivel, on_delete=models.PROTECT)
    estado = models.BooleanField()
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_nivel)

class Ges_CuartoNivel(models.Model):

    descripcion_nivel = models.CharField(max_length=100)
    tercer_nivel = models.ForeignKey(Ges_TercerNivel, on_delete=models.PROTECT)
    estado = models.BooleanField()
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)


    def __str__(self):
        return '{}'.format(self.descripcion_nivel)



def get_full_name(self):
    return self.first_name + ' ' + self.last_name
User.add_to_class("__str__", get_full_name)


class Ges_Niveles (models.Model):
    orden_nivel = models.IntegerField()
    descripcion_nivel = models.CharField(max_length=150)
    estado = models.BooleanField()
    id_primer_nivel= models.ForeignKey(Ges_PrimerNivel, on_delete=models.PROTECT, null=True, blank=True)
    id_segundo_nivel = models.ForeignKey(Ges_SegundoNivel, on_delete=models.PROTECT, null=True, blank=True)
    id_tercer_nivel = models.ForeignKey(Ges_TercerNivel, on_delete=models.PROTECT, null=True, blank=True)
    id_cuarto_nivel = models.ForeignKey(Ges_CuartoNivel, on_delete=models.PROTECT, null=True, blank=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return '{}'.format(self.descripcion_nivel)






