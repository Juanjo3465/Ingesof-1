"""Modulo Reserva"""
from django.db import models

class Reserva(models.Model):
    """"""
    id_reserva = models.AutoField(primary_key=True)
    id_zona_comun = models.ForeignKey('ZonaComun', models.CASCADE, db_column='id_zona_comun')
    id_usuario = models.ForeignKey('core.Usuario', models.CASCADE, db_column='id_usuario')
    fecha_hora = models.DateTimeField()
    cantidad_personas = models.IntegerField()
    duracion = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Reserva'
