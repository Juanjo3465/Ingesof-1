"""Modulo Apartamento"""
from django.db import models
from ..services import AccountService

class Apartamentos(models.Model):
    """"""
    id_apartamento = models.AutoField(primary_key=True)
    interior = models.IntegerField(blank=True, null=True)
    torre = models.IntegerField()
    numero = models.IntegerField()
    id_propietario = models.ForeignKey('Usuario', models.SET_NULL, db_column='id_propietario', blank=True, null=True)
    n_habitaciones = models.IntegerField()
    n_banos = models.IntegerField()
    area_total = models.DecimalField(max_digits=10, decimal_places=2)
    clasificacion = models.CharField(max_length=50, blank=True, null=True)
    deposito = models.IntegerField(blank=True, null=True)
    parqueadero = models.IntegerField(blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Apartamentos'
        unique_together = (('torre', 'numero'),)
        
    @classmethod
    def configure_owner(cls, id_user, id_apartment):
        """"""
        apartment=cls.objects.get(id_apartment)
        
        id_new_owner=id_user
        
        apartment.id_propietario=id_new_owner
        apartment.save()
