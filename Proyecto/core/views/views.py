"""Funciones views de Django"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import Usuario, CodigoRecuperacion
from ..services import LogService, AccountService, AuthenticationService, PasswordService, RecoveryService
from ..services.decorators import login_required, role_required
from .. services.validations import valide_password
from datetime import timezone

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

        recovery = AuthenticationService()
        valid_user = recovery.is_existed_user(username)
        
        if not valid_user:
            context = { 'error' : 'El usuario no existe' }
            return render(request, 'login/confirm_user.html', context)

        token = CodigoRecuperacion.send_authentication_code(username)
        
        if token:
            request.session['reset_token'] = token
            return redirect('Enter_code')
        else:
            context = { 'error' : 'No se pudo enviar el codigo, intentelo nuevamente' }
            return render(request, 'login/confirm_user.html', context)

    return render(request, 'login/confirm_user.html')

def enter_code(request):
    """"""
    back_page = 'Account_info' if request.user.is_authenticated else 'Inicial_page'
    
    context = {}
    context['back_page'] = back_page
    if request.method == 'POST':
        if 'reenviar' in request.POST:        
            # Generar nuevo código
            
            old_token = request.session['reset_token']
            username = CodigoRecuperacion.objects.get(token = old_token).username
            new_token = CodigoRecuperacion.send_authentication_code(username)
            
            if new_token is None:
                context['error'] = 'No se pudo reenviar el codigo, intentelo de nuevo'
                return render(request, 'login/enter_code.html', context)
            
            request.session['reset_token']=new_token
            return render(request, 'login/enter_code.html', context)
        elif 'verificar' in request.POST:
            codigo_ingresado = request.POST.get('codigo')        
            token = request.session['reset_token']
            valide = CodigoRecuperacion.validate_authentication_code(token, codigo_ingresado)
            
            if not valide:
                context['error'] = 'Codigo invalido, intentelo de nuevo o solicite otro codigo'
                return render(request, 'login/enter_code.html', context)

            return redirect('Change_pass')

    return render(request, "login/enter_code.html", context)

@login_required
def change_password(request):
    """"""    
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password', '').strip()
        confirmar_password = request.POST.get('confirmar_password', '').strip()

        if nueva_password != confirmar_password:
            context = {'error': 'Las contraseñas no coinciden',}
            return render(request, 'core/change_password.html', context)
        
        
        mensaje_error = valide_password(nueva_password)
        
        if mensaje_error != "":
            context = { 'error' : mensaje_error }
            return render(request, 'core/change_password.html', context)
        
        service = PasswordService()
        service.change_password(request.user, nueva_password)

        return redirect('Account_info')

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
    """"""
    account=AccountService()
    usuario = account.get_app_user(request.user)
    
    context = {'usuario' : usuario}
    return render(request, 'account/account_info.html', context)

@login_required
def edit_account(request):
    """"""
    account=AccountService()
    usuario = account.get_app_user(request.user)
    context = {'usuario' : usuario}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '')
        correo = request.POST.get('correo', '')
        celular = request.POST.get('celular', '')
        
        errores = account.edit_account_validation(
            nombre, 
            fecha_nacimiento, 
            correo, 
            celular
        )


        if User.objects.filter(username=correo.strip()).exclude(id=request.user.id).exists():
                errores.append('Este correo electrónico ya está registrado')
        
        if errores != []:
            for error in errores:
                messages.error(request, error)
            
            return render(request, 'account/edit_account.html', context)

        try:
            account.edit_account(request, nombre, fecha_nacimiento, correo, celular)
            
            return redirect('Account_info')
        except Exception as e:
            messages.error(request, f'Error al guardar: {str(e)}')
            return render(request, 'account/edit_account.html', context)
    return render(request, 'account/edit_account.html', context)

@login_required
def confirm_password(request):
    if request.method == 'POST':
        if 'siguiente' in request.POST:
            old_password = request.POST.get('old_password')
            
            usuario = request.user.username
            pass_check = AuthenticationService()
            correct_password = pass_check.authenticate(request, usuario, old_password)
            
            if correct_password is None:
                error = "Contraseña incorrecta"
                context = { 'error' : error }
                return render(request, 'login/confirm_password.html', context)
            
            return redirect('Change_pass')
        elif 'olvido' in request.POST:
            token = CodigoRecuperacion.send_authentication_code(request.user.username)
        
            if token:
                request.session['reset_token'] = token
                return redirect('Enter_code')
            else:
                context = { 'error' : 'No se pudo enviar el codigo, intentelo nuevamente' }
                return render(request, 'login/confirm_user.html', context)
            
    return render(request, 'login/confirm_password.html')
