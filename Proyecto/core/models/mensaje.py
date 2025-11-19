"""Modelo Mensaje"""
from django.db import models

class Mensaje(models.Model):
    """"""
    id_mensaje = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField()
    conversacion = models.IntegerField()

    class Meta:
        """"""
        managed = False
        db_table = 'Mensaje'
