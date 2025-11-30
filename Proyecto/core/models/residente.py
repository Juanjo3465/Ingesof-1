"""Modulo Residente"""
from django.db import models
from datetime import date

class Residente(models.Model):
    """"""
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    id_apartamento = models.ForeignKey('Apartamentos', models.CASCADE, db_column='id_apartamento')
    fecha_inicio = models.DateField(blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Residente'
        unique_together = (('id_usuario', 'id_apartamento'),)
    
    @classmethod
    def configure_resident(cls, id_user, id_apartment):
        """"""
        id_new_resident=id_user
        
        resident=cls()
        resident.id_usuario=id_new_resident
        resident.id_apartamento=id_apartment
        resident.fecha_inicio=date.today()
        resident.save()
