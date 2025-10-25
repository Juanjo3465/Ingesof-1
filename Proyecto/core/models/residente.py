from django.db import models

class Residente(models.Model):
    # CORRECCIÓN: Se añade una PK automática y se usa unique_together.
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    id_apartamento = models.ForeignKey('Apartamentos', models.CASCADE, db_column='id_apartamento')
    fecha_inicio = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Residente'
        unique_together = (('id_usuario', 'id_apartamento'),)