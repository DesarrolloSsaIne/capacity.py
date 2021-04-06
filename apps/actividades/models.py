from django.db import models
from apps.periodicidad.models import Glo_Periodicidad
from apps.familia_cargo.models import Glo_FamiliaCargo
from apps.productos.models import Glo_ProductosEstadisticos
from apps.controlador.models import Ges_Controlador
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN, Ges_Objetivo_Operativo
from apps.periodos.models import Glo_Periodos, Glo_validacion, Glo_Seguimiento
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from apps.estado_actividad.models import Glo_EstadoActividad
# Create your models here.
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class Ges_Actividad (models.Model):
    descripcion_actividad= models.CharField(max_length=2000)
    id_periodicidad= models.ForeignKey(Glo_Periodicidad, on_delete=models.PROTECT)
    id_producto_estadistico= models.ForeignKey(Glo_ProductosEstadisticos, on_delete=models.PROTECT, null=True, blank=True)
    horas_actividad= models.CharField(max_length=4)
    volumen= models.CharField(max_length=3)
    personas_asignadas= models.CharField(max_length=3)
    total_horas=models.IntegerField()
    id_familia_cargo= models.ForeignKey(Glo_FamiliaCargo, on_delete=models.PROTECT)
    fecha_inicio_actividad= models.DateField(blank=True, null=True)
    fecha_termino_actividad= models.DateField(blank=True, null=True)
    fecha_registro= models.DateTimeField(auto_now=True)
    id_controlador= models.ForeignKey(Ges_Controlador, on_delete=models.PROTECT)
    estado= models.IntegerField()
    id_periodo= models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, blank=True, null=True)
    id_objetivo_tactico= models.ForeignKey(Ges_Objetivo_Tactico, on_delete=models.PROTECT, blank=True, null=True)
    id_objetivo_tacticotn = models.ForeignKey(Ges_Objetivo_TacticoTN, on_delete=models.PROTECT, blank=True, null=True)
    id_objetivo_operativo = models.ForeignKey(Ges_Objetivo_Operativo, on_delete=models.PROTECT, blank=True, null=True)
    id_estado_actividad = models.ForeignKey(Glo_EstadoActividad, on_delete=models.PROTECT, blank=True, null=True)

    fecha_real_inicio = models.DateField(blank=True, null=True) # Sprint 2 - CI- 10 - 15012021
    fecha_real_termino = models.DateField(blank=True, null=True)
    fecha_reprogramacion_termino = models.DateField(blank=True, null=True)
    fecha_reprogramacion_inicio = models.DateField(blank=True, null=True)
    justificacion = models.CharField(max_length=2000, blank=True, null=True)
    validada = models.IntegerField(blank=True, null=True)
    flag_reporta = models.IntegerField(null=True, blank=True)
    flag_tmp = models.IntegerField(null=True, blank=True)  # Sprint 1 - CI-2 - 11012021
    flag_finalizada = models.IntegerField(null=True, blank=True)  # Sprint 1 - CI-2 - 11012021


class Ges_Observaciones_valida (models.Model):
    descripcion_observacion = models.CharField(max_length=2000)
    id_actividad = models.ForeignKey(Ges_Actividad, on_delete=models.PROTECT, null=True)
    id_periodo_valida = models.ForeignKey(Glo_validacion, on_delete=models.PROTECT, null=True)
    fecha_registro = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} | {}'.format(self.descripcion_observacion)

class Ges_log_reportes(models.Model):
    id_periodo_valida = models.ForeignKey(Glo_validacion, on_delete=models.PROTECT, null=True, blank=True)
    id_actividad = models.ForeignKey(Ges_Actividad, on_delete=models.PROTECT, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_termino = models.DateTimeField(blank=True, null=True)
    fecha_real_termino = models.DateTimeField(blank=True, null=True)
    id_estado_actividad = models.ForeignKey(Glo_EstadoActividad, on_delete=models.PROTECT, null=True, blank=True)


class Ges_Actividad_Historia(models.Model):
    id_periodo_seguimiento= models.ForeignKey(Glo_Seguimiento, on_delete=models.PROTECT, null=True, blank=True)
    id_actividad = models.ForeignKey(Ges_Actividad, on_delete=models.PROTECT, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_reprogramacion_inicio = models.DateTimeField(blank=True, null=True)
    fecha_reprogramacion_termino = models.DateTimeField(blank=True, null=True)

    fecha_real_inicio = models.DateTimeField(blank=True, null=True)  # Sprint 2 - CI- 10 - 15012021
    fecha_real_termino = models.DateTimeField(blank=True, null=True)
    id_estado_actividad = models.ForeignKey(Glo_EstadoActividad, on_delete=models.PROTECT, null=True, blank=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, blank=True, null=True)
    justificacion= models.CharField(max_length=2000, blank=True, null=True)
    id_controlador = models.ForeignKey(Ges_Controlador, blank=True, null=True, on_delete=models.PROTECT)
    validada = models.IntegerField(blank=True, null=True)


