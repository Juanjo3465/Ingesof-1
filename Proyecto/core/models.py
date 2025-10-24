# This is an auto-generated Django model module.
# I've corrected the main issues like composite keys and on_delete rules.

from django.db import models

# Nota: Los modelos de Django (auth_*, django_*) se dejan tal cual, 
# ya que son gestionados internamente por el framework.

class Apartamentos(models.Model):
    id_apartamento = models.AutoField(primary_key=True)
    interior = models.IntegerField(blank=True, null=True)
    torre = models.IntegerField()
    numero = models.IntegerField()
    id_propietario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_propietario', blank=True, null=True)
    n_habitaciones = models.IntegerField()
    n_banos = models.IntegerField()
    area_total = models.DecimalField(max_digits=10, decimal_places=2)
    clasificacion = models.CharField(max_length=50, blank=True, null=True)
    deposito = models.IntegerField(blank=True, null=True)
    parqueadero = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Apartamentos'
        unique_together = (('torre', 'numero'),)


class Asamblea(models.Model):
    id_asamblea = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    lugar = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    doc_convocatoria = models.TextField(blank=True, null=True)
    doc_citacion = models.TextField(blank=True, null=True)
    acta_asamblea = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Asamblea'


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


class Delegado(models.Model):
    # CORRECCIÓN: Se añade una PK automática y se usa unique_together para la restricción.
    id = models.BigAutoField(primary_key=True) 
    id_propietario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_propietario')
    id_asamblea = models.ForeignKey(Asamblea, models.CASCADE, db_column='id_asamblea')
    cedula = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Delegado'
        # CORRECCIÓN: Se asegura que la combinación de propietario y asamblea sea única.
        unique_together = (('id_propietario', 'id_asamblea'),)


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


class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_hora = models.DateTimeField()
    conversacion = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Mensaje'


class Peticion(models.Model):
    id_peticion = models.AutoField(primary_key=True)
    id_asamblea = models.ForeignKey(Asamblea, models.CASCADE, db_column='id_asamblea')
    id_propietario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_propietario')
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_peticion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Peticion'


class Publicacion(models.Model):
    id_publicacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    titulo = models.CharField(max_length=150)
    fecha_publicacion = models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    visibilidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Publicacion'


class Reporte(models.Model):
    # CORRECCIÓN: Se añade una PK automática y se usa unique_together.
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    id_mensaje = models.ForeignKey(Mensaje, models.CASCADE, db_column='id_mensaje')
    motivo = models.CharField(max_length=150)
    comentario = models.TextField(blank=True, null=True)
    fecha_reporte = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Reporte'
        unique_together = (('id_usuario', 'id_mensaje'),)


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_zona_comun = models.ForeignKey('ZonaComun', models.CASCADE, db_column='id_zona_comun')
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    fecha_hora = models.DateTimeField()
    cantidad_personas = models.IntegerField()
    duracion = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Reserva'


class Residente(models.Model):
    # CORRECCIÓN: Se añade una PK automática y se usa unique_together.
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    id_apartamento = models.ForeignKey(Apartamentos, models.CASCADE, db_column='id_apartamento')
    fecha_inicio = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Residente'
        unique_together = (('id_usuario', 'id_apartamento'),)


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    cedula = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    correo = models.CharField(unique=True, max_length=120)
    contrasena = models.CharField(max_length=255)
    celular = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'Usuario'


class UsuarioMensaje(models.Model):
    # CORRECCIÓN: Se añade una PK automática y se usa unique_together.
    id = models.BigAutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.CASCADE, db_column='id_usuario')
    id_mensaje = models.ForeignKey(Mensaje, models.CASCADE, db_column='id_mensaje')
    papel = models.CharField(max_length=8, blank=True, null=True)
    destacado = models.IntegerField(blank=True, null=True)
    leido = models.IntegerField(blank=True, null=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario_Mensaje'
        unique_together = (('id_usuario', 'id_mensaje'),)


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

# ----- Modelos internos de Django (No necesitan cambios) -----
# Es correcto que inspectdb los genere, pero no debes modificarlos.
# Se dejan con managed = False porque Django los gestiona por su cuenta.

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'