from django.db import models

class ZonaComun(models.Model):
    id_zona_comun = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    horario = models.CharField(max_length=100, blank=True, null=True)
    capacidad = models.IntegerField(blank=True, null=True)
    reservacion = models.IntegerField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)
    reglamento_uso = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Zona_comun'