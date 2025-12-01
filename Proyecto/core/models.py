from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone

class asamblea(models.Model):
    ESTADO_CHOICES = [
        ('Programada', 'Programada'),
        ('En curso', 'En curso'),
        ('Finalizada', 'Finalizada'),
        ('Cancelada', 'Cancelada'),
    ]
    
    id_asamblea = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    lugar = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    descripcion = models.TextField(max_length=1000)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Programada')
    doc_convocatoria = models.BinaryField(null=True, blank=True)
    doc_citacion = models.BinaryField(null=True, blank=True)
    doc_acta = models.BinaryField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_hora']
        db_table = 'aseamblea'  # ← CAMBIADO de 'asambleas' a 'aseamblea'
    
    def __str__(self):
        return f"{self.nombre}"


class Propietario(models.Model):
    id_propietario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    apartamentos = models.CharField(max_length=100, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'propietarios'
    
    def __str__(self):
        return self.nombre


class ParticipacionAsamblea(models.Model):
    TIPO_PARTICIPACION = [
        ('Personal', 'Personal'),
        ('Delegado', 'Delegado'),
        ('Ausente', 'Ausente'),
    ]
    
    id_participacion = models.AutoField(primary_key=True)
    asamblea = models.ForeignKey(asamblea, on_delete=models.CASCADE, related_name='participaciones')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='participaciones')
    tipo_participacion = models.CharField(max_length=20, choices=TIPO_PARTICIPACION, default='Personal')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'participaciones_asamblea'
        unique_together = ('asamblea', 'propietario')


class Delegado(models.Model):
    id_delegado = models.AutoField(primary_key=True)
    asamblea = models.ForeignKey(asamblea, on_delete=models.CASCADE, related_name='delegados')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='delegados')
    nombre_delegado = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'delegados'


class Peticion(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Revisada', 'Revisada'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada'),
    ]
    
    id_peticion = models.AutoField(primary_key=True)
    asamblea = models.ForeignKey(asamblea, on_delete=models.CASCADE, related_name='peticiones')
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='peticiones')
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=1000)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'peticiones'
        ordering = ['-fecha_creacion']
