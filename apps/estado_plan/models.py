from django.db import models

# Create your models here.
class Glo_EstadoPlan(models.Model):
    descripcion_estado = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.descripcion_estado)