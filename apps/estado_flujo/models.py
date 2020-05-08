from django.db import models

# Create your models here.
class Glo_EstadoFlujo(models.Model):
    estado= models.IntegerField()
    descripcion_estado = models.CharField(max_length=100)
    flag_nivel=models.IntegerField(null=True)

    def __str__(self):
        return '{}'.format(self.descripcion_estado)