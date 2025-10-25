from django.db import models

class Peticion(models.Model):
    id_peticion = models.AutoField(primary_key=True)
    id_asamblea = models.ForeignKey('Asamblea', models.CASCADE, db_column='id_asamblea')
    id_propietario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_propietario')
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_peticion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Peticion'