from django.db import models

class Publicacion(models.Model):
    id_publicacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('core.Usuario', models.CASCADE, db_column='id_usuario', null=True)
    titulo = models.CharField(max_length=150)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    visibilidad = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, default=0)

    class Meta:
        managed=True
        db_table = 'Publicacion'
        