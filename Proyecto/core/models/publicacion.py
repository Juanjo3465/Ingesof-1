"""Modulo Publicacion"""
from django.db import models

class Publicacion(models.Model):
    """"""
    id_publicacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    titulo = models.CharField(max_length=150)
    fecha_publicacion = models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    visibilidad = models.IntegerField(blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Publicacion'
