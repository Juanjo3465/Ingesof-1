"""Modulo Reporte"""
from django.db import models

class Reporte(models.Model):
    """"""
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey('core.Usuario', models.CASCADE, db_column='id_usuario')
    id_mensaje = models.ForeignKey('Mensaje', models.CASCADE, db_column='id_mensaje')
    motivo = models.CharField(max_length=150)
    comentario = models.TextField(blank=True, null=True)
    fecha_reporte = models.DateTimeField(blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Reporte'
        unique_together = (('id_usuario', 'id_mensaje'),)
