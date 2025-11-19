"""Rol Administradir"""
from .estadoRol import EstadoRol

class Administrador(EstadoRol):
    """"""

    def get_permission(self):
        """"""
        permission="High"
        return permission
