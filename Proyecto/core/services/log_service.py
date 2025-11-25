"""Clase de Log"""
from django.contrib.auth import login as django_login, logout as django_logout
from .authentication_service import AuthenticationService

class LogService:
    """"""

    def login(self, request, username, password):
        """"""
        
        auth=AuthenticationService()
        user = auth.authenticate(request, email=username, password=password)

        if not user:
            return False

        django_login(request, user)
        return True

    def logout(self, request):
        """"""
        django_logout(request)
