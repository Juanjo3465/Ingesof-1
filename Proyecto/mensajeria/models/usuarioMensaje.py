"""Modelo Usuario-Mensaje"""
from django.db import models

class UsuarioMensaje(models.Model):
    """"""
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey('core.Usuario', models.CASCADE, db_column='id_usuario', null=True)
    id_mensaje = models.ForeignKey('Mensaje', models.CASCADE, db_column='id_mensaje', null=True)
    papel = models.CharField(max_length=8, blank=True, null=True)
    destacado = models.IntegerField(blank=True, null=True)
    leido = models.IntegerField(blank=True, null=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Usuario_Mensaje'
        unique_together = (('id_usuario', 'id_mensaje'),)
