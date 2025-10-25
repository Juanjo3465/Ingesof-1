from django.db import models

class DocumentoPublicacion(models.Model):
    # CORRECCIÓN: Se establece id_documento como la clave primaria.
    id_documento = models.AutoField(primary_key=True)
    id_publicacion = models.ForeignKey('Publicacion', models.CASCADE, db_column='id_publicacion')
    nombre = models.CharField(max_length=100)
    extension = models.CharField(max_length=10)
    documento = models.TextField()
    fecha_subida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Documento_Publicacion'