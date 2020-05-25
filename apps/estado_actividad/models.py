from django.db import models

# Create your models here.

class Glo_EstadoActividad(models.Model):
    estado= models.IntegerField()
    descripcion_estado = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.descripcion_estado)