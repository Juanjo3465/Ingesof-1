"""Modulo Conjunto"""
from django.db import models

class Conjunto(models.Model):
    """"""
    id_conjunto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    n_torres = models.IntegerField()
    n_apartamentos = models.IntegerField()

    class Meta:
        """"""
        managed = False
        db_table = 'Conjunto'
   
    @classmethod    
    def get_complex(cls):
        return cls.objects.first()
