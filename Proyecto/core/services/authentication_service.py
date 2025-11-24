"""Clase de autenticacion"""
from django.contrib.auth.models import User
from .password_service import PasswordService
from ..models import Usuario


class AuthenticationService:
    """"""

    def __init__(self,password_service=None):
        if password_service is None: 
            self.password_service = PasswordService()
        else:
            self.password_service=password_service

    def authenticate(self, request, email=None, password=None):
        """Verifica las credenciales del usuario"""

        try:
            usuario = Usuario.objects.get(correo=email)
        except Usuario.DoesNotExist:
            return None

        if not self.password_service.verify_password(password, usuario.contrasena):
            return None

        user_django, created = User.objects.get_or_create(
            username=usuario.correo,
        )

        if created:
            user_django.set_unusable_password()
            user_django.save()

        user_django.role = usuario.get_rol

        return user_django

    def get_user(self, user_id):
        """Devuelve el usuario y el rol de este, se utiliza en cada request"""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        try:
            usuario = Usuario.objects.get(correo=user.email)
            user.role = usuario.get_rol
        except Usuario.DoesNotExist:
            return None

        return user
