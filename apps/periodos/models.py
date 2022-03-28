from django.db import models
from apps.estado_seguimiento.models import Glo_EstadoSeguimiento
# Create your models here.

# Create your models here.
class Glo_EstadoPeriodo(models.Model):
    estado= models.IntegerField()
    descripcion_periodo= models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.descripcion_periodo)


class Glo_Periodos(models.Model):
    descripcion_periodo = models.CharField(max_length=100)
    anio_periodo= models.IntegerField()
    fecha_inicio=models.DateField(blank=True, null=True)
    fecha_termino=models.DateField(blank=True, null=True)
    id_estado = models.ForeignKey(Glo_EstadoPeriodo, on_delete=models.PROTECT, null=True)


    def __str__(self):
        return '{}'.format(self.descripcion_periodo)



class Glo_Seguimiento(models.Model):
    id_periodo= models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True, blank=True)
    fecha_inicio= models.DateTimeField(blank=True, null=True)
    fecha_termino= models.DateTimeField(blank=True, null=True)
    descripcion_seguimiento = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio_corte=models.DateField(blank=True, null=True)
    fecha_termino_corte=models.DateField(blank=True, null=True)

    id_estado_seguimiento= models.ForeignKey(Glo_EstadoSeguimiento, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion_seguimiento)

class Glo_validacion(models.Model):
    id_periodo= models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True, blank=True)
    id_periodo_seguimiento = models.ForeignKey(Glo_Seguimiento, on_delete=models.PROTECT, null=True, blank=True)
    fecha_inicio= models.DateTimeField(blank=True, null=True)
    fecha_termino= models.DateTimeField(blank=True, null=True)
    id_estado_periodo= models.ForeignKey(Glo_EstadoSeguimiento, on_delete=models.PROTECT, null=True, blank=True)
    descripcion_validacion = models.CharField(max_length=100, null=True, blank=True)



class RespaldoPeriodo(models.Model):
    id_pn = models.IntegerField(blank=True, null=True)
    primer_nivel = models.CharField(max_length=500, blank=True, null=True)
    id_sn = models.IntegerField(blank=True, null=True)
    segundo_nivel = models.CharField(max_length=500, blank=True, null=True)
    id_tni = models.IntegerField(blank=True, null=True)
    tercer_nivel = models.CharField(max_length=500, blank=True, null=True)
    id_cn = models.IntegerField(blank=True, null=True)
    cuarto_nivel = models.CharField(max_length=500, blank=True, null=True)
    ejes = models.CharField(max_length=500, blank=True, null=True)
    id_oe = models.IntegerField(blank=True, null=True)
    objetivo_estrategico = models.CharField(max_length=500, blank=True, null=True)
    id_ot = models.IntegerField(blank=True, null=True)
    objetivo_tactico = models.CharField(max_length=500, blank=True, null=True)
    id_tn = models.IntegerField(blank=True, null=True)
    objetivo_tacticotn = models.CharField(max_length=500, blank=True, null=True)
    id_op = models.IntegerField(blank=True, null=True)
    objetivo_operativo = models.CharField(max_length=500, blank=True, null=True)
    id_actividad = models.IntegerField(blank=True, null=True)
    descripcion_actividad = models.CharField(max_length=500, blank=True, null=True)
    horas_actividad = models.IntegerField(blank=True, null=True)
    volumen = models.IntegerField(blank=True, null=True)
    personas_asignadas = models.IntegerField(blank=True, null=True)
    total_horas = models.IntegerField(blank=True, null=True)
    fecha_inicio_actividad = models.DateField(blank=True, null=True)
    fecha_termino_actividad = models.DateField(blank=True, null=True)
    fecha_registro = models.DateField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    fecha_real_inicio = models.DateField(blank=True, null=True)
    fecha_real_termino = models.DateField(blank=True, null=True)
    fecha_reprogramacion_termino = models.DateField(blank=True, null=True)
    justificacion = models.CharField(max_length=2500, blank=True, null=True)
    validada = models.CharField(max_length=50, blank=True, null=True)
    flag_tmp = models.IntegerField(blank=True, null=True)
    flag_reporta = models.IntegerField(blank=True, null=True)
    descripcion_estado = models.CharField(max_length=50, blank=True, null=True)
    descripcion_familiacargo = models.CharField(max_length=50, blank=True, null=True)
    descripcion_periodicidad = models.CharField(max_length=50, blank=True, null=True)
    id_gp = models.IntegerField(blank=True, null=True)
    descripcion_periodo = models.CharField(max_length=50, blank=True, null=True)
    anio_periodo = models.IntegerField(blank=True, null=True)
    fecha_inicio_periodo = models.DateField(blank=True, null=True)
    fecha_termino_periodo = models.DateField(blank=True, null=True)
    producto_estadistico = models.CharField(max_length=150, blank=True, null=True)
    flag_finalizada = models.IntegerField(blank=True, null=True)
    jefatura = models.CharField(max_length=150, blank=True, null=True)
    estado_flujo_controlador = models.CharField(max_length=150, blank=True, null=True)
    estado_plan_controlador = models.CharField(max_length=150, blank=True, null=True)
    analista_asignado = models.CharField(max_length=150, blank=True, null=True)
    primera_revision = models.CharField(max_length=150, blank=True, null=True)
    segunda_revision = models.CharField(max_length=150, blank=True, null=True)
