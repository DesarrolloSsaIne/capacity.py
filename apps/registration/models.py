from django.db import models
from django.contrib.auth.models import User

class logAcceso(models.Model):
    user = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

class logEventos(models.Model):

    fecha_evento = models.DateTimeField(auto_now=True)
    tipo_evento= models.CharField( max_length=500, blank=True, null=True)
    metodo= models.CharField( max_length=500, blank=True, null=True)
    usuario_evento= models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="usuario_evento")
    jefatura_dirigida = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="jefatura_dirigida")


