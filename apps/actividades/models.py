from django.db import models
from apps.periodicidad.models import Glo_Periodicidad
from apps.familia_cargo.models import Glo_FamiliaCargo
from apps.productos.models import Glo_ProductosEstadisticos
from apps.controlador.models import Ges_Controlador
from apps.objetivos.models import Ges_Objetivo_Estrategico, Ges_Objetivo_Tactico, Ges_Objetivo_TacticoTN, Ges_Objetivo_Operativo
from apps.periodos.models import Glo_Periodos
from apps.estado_actividad.models import Glo_EstadoActividad
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class Ges_Actividad (models.Model):
    descripcion_actividad= models.CharField(max_length=2000)
    id_periodicidad= models.ForeignKey(Glo_Periodicidad, on_delete=models.PROTECT)
    id_producto_estadistico= models.ForeignKey(Glo_ProductosEstadisticos, on_delete=models.PROTECT)
    horas_actividad= models.CharField(max_length=4)
    volumen= models.CharField(max_length=3)
    personas_asignadas= models.CharField(max_length=3)
    total_horas=models.IntegerField()
    id_familia_cargo= models.ForeignKey(Glo_FamiliaCargo, on_delete=models.PROTECT)
    fecha_inicio_actividad= models.DateField()
    fecha_termino_actividad= models.DateField()
    fecha_registro= models.DateTimeField(auto_now=True)
    id_controlador= models.ForeignKey(Ges_Controlador, on_delete=models.PROTECT)
    estado= models.IntegerField()
    id_periodo= models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, blank=True, null=True)
    id_objetivo_tactico= models.ForeignKey(Ges_Objetivo_Tactico, on_delete=models.PROTECT, blank=True, null=True)
    id_objetivo_tacticotn = models.ForeignKey(Ges_Objetivo_TacticoTN, on_delete=models.PROTECT, blank=True, null=True)
    id_objetivo_operativo = models.ForeignKey(Ges_Objetivo_Operativo, on_delete=models.PROTECT, blank=True, null=True)
    id_estado_actividad = models.ForeignKey(Glo_EstadoActividad, on_delete=models.PROTECT, blank=True, null=True)

    fecha_real_termino = models.DateField(blank=True, null=True)
    fecha_reprogramacion_termino = models.DateField(blank=True, null=True)
    fecha_reprogramacion_inicio = models.DateField(blank=True, null=True)
    justificacion = models.CharField(max_length=2000, blank=True, null=True)
