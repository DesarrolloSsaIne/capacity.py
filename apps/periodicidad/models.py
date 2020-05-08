from django.db import models

# Create your models here.

class Glo_Periodicidad(models.Model):
    descripcion_periodicidad = models.CharField(max_length=200)

    def __str__(self):
        return '{} '.format( self.descripcion_periodicidad)