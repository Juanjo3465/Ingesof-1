"""Modulo Usuario"""
from django.db import models
from functools import cached_property
from ..domain.states.roles import Administrador, Propietario, Residente

class Usuario(models.Model):
    """"""
    
    Rol_Administrador=Administrador.get_name()
    Rol_Propietario=Propietario.get_name()
    Rol_Residente=Residente.get_name()
    
    id_usuario = models.AutoField(primary_key=True)
    cedula = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    correo = models.CharField(unique=True, max_length=120)
    contrasena = models.CharField(max_length=255)
    celular = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=11)
    
    @cached_property
    def get_rol(self):
        """"""
        Roles={
            self.Rol_Administrador:Administrador,
            self.Rol_Propietario:Propietario,
            self.Rol_Residente:Residente,    
        }

        return Roles[self.rol]

    class Meta:
        """"""
        managed = False
        db_table = 'Usuario'
