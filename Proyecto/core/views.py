from django.shortcuts import render, redirect
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Falta logica de login
    
    return render(request, 'core/login_interface.html')

def confirm_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # Falta logica de confirmar usuario y enviar email (posible token)
        
        return redirect('Enter_code')
        
    
    return render(request, 'core/confirm_user.html')

def enter_code(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')
        
        # Falta logica de verificar y reenviar codigo
        
        return redirect('Change_pass')
    
    return render(request, "core/enter_code.html")

def change_password(request):    
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')
        
        # Falta logica de confirmar contraseña

    return render(request, 'core/change_password.html')


def hola(request):
    return HttpResponse("Hola Django, la app core está funcionando ✅")
# Create your views here.
