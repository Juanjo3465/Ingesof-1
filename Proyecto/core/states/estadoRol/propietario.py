from .estadoRol import EstadoRol

class Propietario(EstadoRol):
    
    def get_permission(self):
        permission="Medium"
        return permission