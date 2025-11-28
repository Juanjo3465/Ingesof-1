"""Modulo asamblea"""
from django.db import models

class Asamblea(models.Model):
    """"""
    id_asamblea = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    lugar = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    doc_convocatoria = models.TextField(blank=True, null=True)
    doc_citacion = models.TextField(blank=True, null=True)
    acta_asamblea = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Asamblea'
