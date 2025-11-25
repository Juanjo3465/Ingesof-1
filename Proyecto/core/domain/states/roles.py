"""Roles del usuario"""
from abc import ABC, abstractmethod

class Role(ABC):
    """Interfaz base para el patrón State basado en roles"""

    @abstractmethod
    def get_name():
        """"""
        pass

class Administrador(Role):
    """"""
    @classmethod
    def get_name(cls):
        """"""
        return 'Admin'
    
class Propietario(Role):
    """"""
    @classmethod
    def get_name(cls):
        """"""
        return 'Propietario'

class Residente(Role):
    """"""
    @classmethod
    def get_name(cls):
        """"""
        return 'Residente'
