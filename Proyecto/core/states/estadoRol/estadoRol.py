from abc import ABC, abstractmethod

class EstadoRol(ABC):
    """Interfaz base para el patrón State basado en roles"""
    
    @abstractmethod
    def get_permission(self):
        pass
    
