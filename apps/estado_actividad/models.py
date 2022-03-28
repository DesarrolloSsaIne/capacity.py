from django.db import models

# Create your models here.

class Glo_EstadoActividad(models.Model):
    descripcion_estado = models.CharField(max_length=100)
    orden=models.IntegerField(null=True, blank=True)
    descripcion_validada=models.CharField(max_length=50,null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.descripcion_estado)

