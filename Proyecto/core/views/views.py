"""Funciones views de Django"""
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from ..models import Usuario, Apartamentos
from ..services import LogService
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import Usuario, CodigoRecuperacion, Conjunto
from ..services import LogService, AccountService, AuthenticationService, PasswordService, ApartmentService
from ..services import ApartmentFilter
from ..services.decorators import login_required, role_required
from django.contrib import messages
from ..services.services import *
from ..services.validations import *


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
            return redirect('forum')

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
def logout(request):
    """"""
    if request.method == 'POST':
        auth=LogService()
        auth.logout(request)
        return redirect('Inicial_page')
    return redirect('forum')

@login_required
def account_info(request):
    """"""
    account=AccountService()
    usuario = account.get_app_user(request.user)
    
    context = {'usuario' : usuario}
    return render(request, 'account/account_info.html', context)
    
@role_required(Usuario.Rol_Administrador)
def gestion_usuarios_view(request):
    
    return render(request, 'core/gestion_usuarios.html')

@role_required(Usuario.Rol_Administrador)
def crear_usuario_view(request):
    if request.method == 'POST':

        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        celular = request.POST.get('celular')
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get('rol')
        apartamento_id = request.POST.get('apartamento') 

        if not all([cedula, nombre, correo, contrasena, rol]):
            messages.error(request, 'Todos los campos excepto Celular y Fecha de Nacimiento son obligatorios.')
            return redirect('crear_usuario')
        
        if validar_correo(correo) != "":
            messages.error(request, f'El formato del correo "{correo}" no es válido.')
            return redirect('crear_usuario')
            
        if valide_password(contrasena) != "":
            messages.error(request, 'La contraseña no cumple los requisitos de seguridad (mín. 8 caracteres, una mayúscula, una minúscula y un número).')
            return redirect('crear_usuario')
        
        fecha_nacimiento_obj = validar_fecha_nacimiento(fecha_nacimiento_str)
        if fecha_nacimiento_str and fecha_nacimiento_obj != "":
            messages.error(request, 'La fecha de nacimiento es inválida o está fuera del rango permitido.')
            return redirect('crear_usuario')

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, f'El correo "{correo}" ya está registrado.')
            return redirect('crear_usuario')
        
        if Usuario.objects.filter(cedula=cedula).exists():
            messages.error(request, f'La cédula "{cedula}" ya está registrada.')
            return redirect('crear_usuario')            
            
        try:
            with transaction.atomic():
                password_service = PasswordService()
                contrasena_hasheada = password_service.hash_password(contrasena)

                nuevo_usuario = Usuario.objects.create(
                    cedula=cedula,
                    nombre=nombre,
                    correo=correo,
                    celular=celular,
                    fecha_nacimiento=fecha_nacimiento_str, # objeto 'date' validado
                    contrasena=contrasena_hasheada,
                    rol=rol
                )
                
                messages.success(request, f'Usuario "{nombre}" creado con éxito.')
                
                if rol in ['Propietario', 'Residente']:
                    
                    apartamento_obj = Apartamentos.objects.get(pk=apartamento_id)
                    configure_apartment(nuevo_usuario, apartamento_obj)
                    
                    messages.info(request, f'El usuario fue asociado correctamente al apartamento {apartamento_obj}.')

                return redirect('crear_usuario') 

        except Apartamentos.DoesNotExist:
            messages.error(request, 'El apartamento seleccionado no es válido.')
            return redirect('crear_usuario')
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado al crear el usuario: {e}')
            return redirect('crear_usuario')

    context = {
        'apartamentos' : Apartamentos.objects.all() 
    }
    return render(request, 'core/admin_crear_usuario.html',context)

@role_required(Usuario.Rol_Administrador)
def buscar_usuario_admin_view(request):
    """
    Gestiona la búsqueda y listado de usuarios para el administrador.
    Permite filtrar por correo.
    """
    if request.method == 'POST':
        ids_a_eliminar = request.POST.getlist('usuarios_a_eliminar')

        if not ids_a_eliminar:
            messages.warning(request, 'No ha seleccionado ningún usuario para eliminar.')
        else:
            usuarios_para_borrar = Usuario.objects.filter(
                pk__in=ids_a_eliminar
            ).exclude(correo=request.user.username)

            count = usuarios_para_borrar.count()
            if count > 0:
                usuarios_para_borrar.delete()
                messages.success(request, f'Se han eliminado {count} usuario(s) con éxito.')
            elif count == 0 and ids_a_eliminar:
                messages.error(request, 'No se pudo eliminar a los usuarios seleccionados (posiblemente intentó eliminarse a sí mismo).')
        
        return redirect('buscar_usuario')
    
    query_correo = request.GET.get('correo_buscado', '') 
    usuarios_list = Usuario.objects.all().exclude(correo=request.user.username).order_by('nombre')

    if query_correo:
        usuarios_list = usuarios_list.filter(correo__icontains=query_correo)

    contexto = {
        'usuarios': usuarios_list,
        'query_correo_actual': query_correo 
    }
    
    return render(request, 'core/admin_buscar_usuario.html', contexto)

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

@login_required
def complex_info(request):
    """"""
    conjunto=Conjunto.get_complex()
    context={'conjunto':conjunto}
    return render(request, 'complex_info.html', context)

@role_required(Usuario.Rol_Residente)
def resident_apartment(request):
    """
    Vista para mostrar la información del apartamento del residente
    """
    
    user = request.user
    
    apartment = ApartmentService()
    my_aparment=apartment.get_resident_apartment(user)
    
    if my_aparment is None:
        return render(request, 'apartment/resident_apartment.html')
    
    context = {
        'apartment': my_aparment
    }
    
    return render(request, 'apartment/resident_apartment.html', context)

@role_required(Usuario.Rol_Propietario)
def owner_apartment(request):
    """
    Vista para listar los apartamentos del propietario logueado.
    """
    apartment_service = ApartmentService()
    
    apartamentos = apartment_service.get_owner_apartments(request.user)
    
    if apartamentos:
        apartamentos = apartamentos.order_by('interior', 'torre', 'numero')
        
    context={
        'apartamentos': apartamentos
    }
    
    return render(request, 'apartment/owner_apartment.html', context)

@role_required(Usuario.Rol_Propietario)
def owner_apartment_info(request, id_apartamento):
    """
    Vista para mostrar el detalle de un apartamento del propietario logueado.
    Solo el propietario del apartamento puede acceder a esta vista.
    """
    apartamento = get_object_or_404(Apartamentos, id_apartamento=id_apartamento)
    
    account_service = AccountService()
    usuario = account_service.get_app_user(request.user)
    
    if apartamento.id_propietario != usuario:
        return redirect('Owner_apartment')
    
    apartment_service = ApartmentService()
    residentes = apartment_service.get_residents(apartamento)
    
    context = {
        'apartamento': apartamento,
        'residentes': residentes
    }
    
    return render(request, 'apartment/owner_apartment_info.html', context)

@role_required(Usuario.Rol_Administrador)
def admin_apartment(request):
    """
    Vista para buscar apartamentos con filtros opcionales.
    """
    filtro = ApartmentFilter(
        Apartamentos.objects.select_related('id_propietario').all(),
        request.GET
    )
    
    apartamentos = filtro.apply().order_by('interior', 'torre', 'numero')
    
    context={
        'apartamentos': apartamentos
    }
    
    return render(request, 'apartment/admin_apartment.html', context)

@role_required(Usuario.Rol_Administrador)
def admin_apartment_info(request, id_apartamento):
    """
    Vista para mostrar el detalle completo de un apartamento para el admin
    """
    apartamento = get_object_or_404(Apartamentos, id_apartamento=id_apartamento)
    
    service = ApartmentService()
    propietario = service.get_owner(apartamento)
    residentes = service.get_residents(apartamento)
    
    context = {
        'apartamento': apartamento,
        'propietario': propietario,
        'residentes': residentes
    }
    
    return render(request, 'apartment/admin_apartment_info.html', context)