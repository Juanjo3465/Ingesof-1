from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario 

# Clase Singleton para manejar acceso centralizado 
class UsuarioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls) 
        return cls._instance

    def listar_todos(self):
        return Usuario.objects.all()

# Vista que utiliza el Singleton 
def listar_usuarios(request):
    manager = UsuarioManager() 
    usuarios = manager.listar_todos() 
    contexto = {'usuarios': usuarios}
    return render(request, 'core/listar_usuarios.html', contexto)

def header_user(request):
    return render(request, 'core/header_user.html')


def hola(request):
    return HttpResponse("Hola Django, la app core está funcionando ✅")
# Create your views here.
