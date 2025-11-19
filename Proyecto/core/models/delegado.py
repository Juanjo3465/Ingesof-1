"""Modelo Delegado"""
from django.db import models

class Delegado(models.Model):
    """"""
    # CORRECCIÓN: Se añade una PK automática y se usa unique_together para la restricción.
    id = models.BigAutoField(primary_key=True) 
    id_propietario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_propietario')
    id_asamblea = models.ForeignKey('Asamblea', models.CASCADE, db_column='id_asamblea')
    cedula = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)

    class Meta:
        """"""
        managed = False
        db_table = 'Delegado'
        # CORRECCIÓN: Se asegura que la combinación de propietario y asamblea sea única.
        unique_together = (('id_propietario', 'id_asamblea'),)
