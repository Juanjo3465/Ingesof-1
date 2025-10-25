from django.db import models

class Conjunto(models.Model):
    id_conjunto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    n_torres = models.IntegerField()
    n_apartamentos = models.IntegerField()
    n_parqueaderos = models.IntegerField()
    reglamento_propiedad_horizontal = models.TextField(blank=True, null=True)
    estatutos = models.TextField(blank=True, null=True)
    manual_convivencia = models.TextField(blank=True, null=True)
    estado_financiero = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Conjunto'