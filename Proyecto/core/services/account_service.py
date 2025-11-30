"""Servicios de cuenta"""
from django.contrib.auth.models import User
from django.db import transaction
from ..models import Usuario
from .validations import validar_nombre, validar_correo, validar_celular, validar_fecha_nacimiento

class AccountService():
    """"""
    def get_app_user(self,user:User):
        """Obtner el regitro de la base de datos de usuario"""
        email=user.username
        
        try:
            user_app=Usuario.objects.get(correo=email)
        except Usuario.DoesNotExist:
            return None
        
        return user_app
    
    def get_app_user_register(self, username):
        try:
            user_app=Usuario.objects.get(correo=username)
        except Usuario.DoesNotExist:
            return None
        
        return user_app
    
    def edit_account_validation(self,nombre: str, fecha_nacimiento, correo: str, celular: str):
        """ Valida todos los campos del formulario de editar cuenta """
        
        errores = []
        
        error = validar_nombre(nombre)
        if error != "":
            errores.append(error)
        
        error = validar_fecha_nacimiento(fecha_nacimiento)
        if error != "":
            errores.append(error)
        
        error = validar_correo(correo)
        if error != "":
            errores.append(error)
        
        error = validar_celular(celular)
        if error != "":
            errores.append(error)
        
        return errores
    
    def edit_account(self, request, nombre, fecha_nacimiento, correo, celular):
        with transaction.atomic():
            usuario = self.get_app_user(request.user)
            usuario.nombre = nombre.strip()
            usuario.fecha_nacimiento = fecha_nacimiento
            usuario.correo = correo.strip()
            usuario.celular = celular.strip()
            usuario.save()

            request.user.username = correo
            request.user.save()
        
        
        