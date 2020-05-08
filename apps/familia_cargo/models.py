from django.db import models

class Glo_FamiliaCargo(models.Model):
    descripcion_familiacargo= models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.descripcion_familiacargo)