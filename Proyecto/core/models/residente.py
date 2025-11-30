"""Modulo Residente"""
from django.db import models
from datetime import date
#from ..services import AccountService

class Residente(models.Model):
    """"""
    id_usuario = models.ForeignKey(
        'Usuario', 
        models.CASCADE, 
        db_column='id_usuario', 
        unique=True,
        primary_key=True # <-- ¡CRUCIAL!
    )
    id_apartamento = models.ForeignKey('Apartamentos', models.CASCADE, db_column='id_apartamento')
    fecha_inicio = models.DateField(blank=True, null=True)

    class Meta:
        """"""
        managed = False
        db_table = 'Residente'
        unique_together = (('id_usuario', 'id_apartamento'),)
    
    @classmethod
    def configure_resident(cls, id_user, id_apartment):
        """"""
        try:
            cls.objects.create(
                # ¡LA CLAVE! Le decimos a Django: "Para la FK 'id_usuario',
                # usa este valor de ID directamente".
                id_usuario = id_user,
                
                # Hacemos lo mismo para la FK del apartamento.
                id_apartamento = id_apartment,
                
                fecha_inicio = date.today()
            )
            print(f"Registro de Residente creado para el usuario ID {id_user}")
            print(f"El apartamento para este es  {id_apartment}")
        except Exception as e:
            # Capturamos posibles IntegrityError si el apartamento no existe, etc.
            print(f"Error al crear el registro de Residente: {e}")
