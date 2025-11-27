"""Funciones views de Django"""
from django.shortcuts import render, redirect
from ..models import Usuario
from ..services import LogService
from ..services.decorators import login_required, role_required

class UsuarioManager:
    """"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def listar_todos(self):
        """"""
        return Usuario.objects.all()

def inicial_page(request):
    return render(request, 'core/inicial_page.html')

def login_view(request):
    """"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        log=LogService().login(request, username, password)
        
        if log:
            return redirect('Header_user')

        context= {
            "error": "Usuario o contraseña incorrecta",
            "username": username
        }
        
        return render(request, 'core/login_interface.html', context)
        
    return render(request, 'core/login_interface.html')

def confirm_user(request):
    """"""
    if request.method == 'POST':
        username = request.POST.get('username')

        # Falta logica de confirmar usuario y enviar email (posible token)

        return redirect('Enter_code')

    return render(request, 'core/confirm_user.html')

def enter_code(request):
    """"""
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')

        # Falta logica de verificar y reenviar codigo

        return redirect('Change_pass')

    return render(request, "core/enter_code.html")

def change_password(request):
    """"""
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')

        # Falta logica de confirmar contraseña

    return render(request, 'core/change_password.html')

@role_required(Usuario.Rol_Administrador)
def listar_usuarios(request):
    """"""
    manager = UsuarioManager()
    usuarios = manager.listar_todos()
    contexto = {'usuarios': usuarios, 'user_django': request.user}
    return render(request, 'core/listar_usuarios.html', contexto)

@login_required
def header_user(request):
    """"""
    return render(request, 'header_user.html')
