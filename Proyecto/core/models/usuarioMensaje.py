from django.db import models

class UsuarioMensaje(models.Model):
    # CORRECCIÓN: Se añade una PK automática y se usa unique_together.
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    id_mensaje = models.ForeignKey('Mensaje', models.CASCADE, db_column='id_mensaje')
    papel = models.CharField(max_length=8, blank=True, null=True)
    destacado = models.IntegerField(blank=True, null=True)
    leido = models.IntegerField(blank=True, null=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario_Mensaje'
        unique_together = (('id_usuario', 'id_mensaje'),)