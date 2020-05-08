from django.db import models
from apps.estructura.models import Ges_Niveles, Ges_PrimerNivel, Ges_SegundoNivel, Ges_TercerNivel, Ges_CuartoNivel
from django.contrib.auth.models import User
from apps.periodos.models import Glo_Periodos
# Create your models here.

class Ges_Jefatura(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.PROTECT)
    id_nivel = models.ForeignKey(Ges_Niveles, on_delete=models.PROTECT, null=True)
    id_periodo = models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{}   |   {}'.format( self.id_nivel, self.id_user)







