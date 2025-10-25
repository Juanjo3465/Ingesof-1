from django.db import models


class DocumentoMensaje(models.Model):
    # CORRECCIÓN: Se establece id_documento como la clave primaria.
    id_documento = models.AutoField(primary_key=True)
    id_mensaje = models.ForeignKey('Mensaje', models.CASCADE, db_column='id_mensaje')
    nombre = models.CharField(max_length=100, blank=True, null=True)
    extension = models.CharField(max_length=10)
    documento = models.TextField()
    fecha_subida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Documento_Mensaje'