"""Roles del usuario"""
from abc import ABC, abstractmethod

class Role(ABC):
    """Interfaz base para el patrón State basado en roles"""

    @abstractmethod
    def get_name(self):
        """"""
        pass

class Administrador(Role):
    """"""
    
    def get_name(self):
        """"""
        return 'Admin'
    
class Propietario(Role):
    """"""
    def get_name(self):
        """"""
        return 'Propietario'

class Residente(Role):
    """"""
    def get_name(self):
        """"""
        return 'Residente'
