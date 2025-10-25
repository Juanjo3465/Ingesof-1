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
    
    _estado_rol=None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._estado_rol=self.get_state()
        
    def get_state(self):
        
        state={
            'Admin':Administrador(),
            'Propietario':Propietario(),
            'Residente':Residente()    
        }
        
        return state[self.rol]
    
    def get_permission(self):
        return self._estado_rol.get_permission()
        

    class Meta:
        managed = False
        db_table = 'Usuario'