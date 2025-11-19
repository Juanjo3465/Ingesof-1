"""Rol Residente"""
from .estadoRol import EstadoRol

class Residente(EstadoRol):
    """"""
    def get_permission(self):
        """"""
        permission="Low"
        return permission
