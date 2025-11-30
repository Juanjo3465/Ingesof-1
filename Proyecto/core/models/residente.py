"""Modulo Residente"""
from django.contrib.auth.models import User
from django.db import models
from datetime import date
from .apartamentos import Apartamentos


class Residente(models.Model):
    """"""
    id_usuario = models.ForeignKey(
        'Usuario', 
        models.CASCADE, 
        db_column='id_usuario', 
        unique=True,
        primary_key=True
    )
    id_apartamento = models.ForeignKey('Apartamentos', models.CASCADE, db_column='id_apartamento')
    fecha_inicio = models.DateField(blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Residente'
        unique_together = (('id_usuario', 'id_apartamento'),)
        
    @classmethod
    def get_apartment(cls, user:User):
        from ..services import AccountService
        account = AccountService()
        usuario = account.get_app_user(user)
        
        try:
            residencia = cls.objects.get(id_usuario=usuario.id_usuario)
        except cls.DoesNotExist:
            return None
        
        apartment = Apartamentos.objects.get(id_apartamento=residencia.id_apartamento)
        return apartment
    
    @classmethod
    def configure_resident(cls, id_user, id_apartment):
        """"""
        try:
            cls.objects.create(
                id_usuario = id_user,
                id_apartamento = id_apartment,
                fecha_inicio = date.today()
            )
            print(f"Registro de Residente creado para el usuario {id_user}")
        except Exception as e:
            print(f"Error al crear el registro de Residente: {e}")
