from django.db import models
from core.states.estadoRol import Administrador, Residente, Propietario

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    cedula = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    correo = models.CharField(unique=True, max_length=120)
    contrasena = models.CharField(max_length=255)
    celular = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=11)
    
    
    class Meta:
        db_table = 'Usuario'