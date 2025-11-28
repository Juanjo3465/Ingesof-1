"""Funciones views de Django"""
from django.shortcuts import render, redirect
from ..models import Usuario
from ..services import LogService
from ..services.decorators import login_required, role_required
from ..services.services import get_app_user

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
    return render(request, 'inicial_page.html')

def login(request):
    """"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        log=LogService().login(request, username, password)
        
        if log:
            return redirect('Menu')

        context= {
            "error": "Usuario o contraseña incorrecta",
            "username": username
        }
        
        return render(request, 'login/login_interface.html', context)
        
    return render(request, 'login/login_interface.html')

def confirm_user(request):
    """"""
    if request.method == 'POST':
        username = request.POST.get('username')

        # Falta logica de confirmar usuario y enviar email (posible token)

        return redirect('Enter_code')

    return render(request, 'login/confirm_user.html')

def enter_code(request):
    """"""
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo')

        # Falta logica de verificar y reenviar codigo

        return redirect('Change_pass')

    return render(request, "login/enter_code.html")

def change_password(request):
    """"""
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')

        # Falta logica de confirmar contraseña

    return render(request, 'login/change_password.html')

@role_required(Usuario.Rol_Administrador)
def listar_usuarios(request):
    """"""
    manager = UsuarioManager()
    usuarios = manager.listar_todos()
    contexto = {'usuarios': usuarios, 'user_django': request.user}
    return render(request, 'listar_usuarios.html', contexto)

@login_required
def menu(request):
    """"""
    return render(request, 'base_menu.html')

@login_required
def logout(request):
    """"""
    if request.method == 'POST':
        auth=LogService()
        auth.logout(request)
        return redirect('Inicial_page')
    return redirect('Menu')

@login_required
def account_info(request):
    usuario = get_app_user(request.user)
    
    context = {'usuario' : usuario}
    return render(request, 'account/account_info.html', context)
    