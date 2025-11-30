"""Modulo Apartamento"""
from django.db import models
#from ..services import AccountService

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
    def configure_owner(cls, user_obj, obj_apartment):
        """
        Asigna un usuario como propietario de un apartamento específico.
        Recibe el OBJETO de usuario completo y el OBJETO del apartamento tambien.
        """
        try:
            apartment = obj_apartment
            apartment.id_propietario = user_obj
            apartment.save()
            
            print(f"Usuario {user_obj.nombre} asignado como propietario del Apartamento ID {obj_apartment.id_apartamento}")

        except cls.DoesNotExist:
            print(f"Error: No se encontró un apartamento con ID {obj_apartment.id_apartamento}")
        except Exception as e:
            print(f"Ocurrió un error inesperado en configure_owner cansonnn: {e}")