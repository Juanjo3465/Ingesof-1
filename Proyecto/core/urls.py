"""Urls del core del proyecto"""
from django.urls import path
from core.views import views, verify_session

urlpatterns = [
    path('Usuarios/', views.listar_usuarios, name='lista_de_usuarios'),
    path('', views.inicial_page, name='Inicial_page'),
    path('Login/', views.login, name='Login'),
    path('Login/Confirmar-usuario/', views.confirm_user, name='Confirm_user'),
    path('Recuperar-contraseña/', views.enter_code, name='Enter_code'),
    path('Cambiar-contraseña/', views.change_password, name='Change_pass'),
    path('Logout/', views.logout, name='Logout'),
    path('Verificar-sesion/', verify_session, name='Verify_session' ),
    path('Mi-cuenta/', views.account_info, name='Account_info'),
    path('Editar-cuenta/', views.edit_account, name = 'Edit_account'),
    path('Confirmar-contrasena', views.confirm_password, name = 'Confirm_password'),
    path('Conjunto/', views.complex_info, name='Complex_info' ),
    path('gestion-usuario/', views.gestion_usuarios_view, name='gestion_usuario'),
    path('crear_usuario/', views.crear_usuario_view, name='crear_usuario'),
    path('buscar_usuario/', views.buscar_usuario_admin_view, name='buscar_usuario'),
    path('Apartamento/Residente/', views.resident_apartment, name='Resident_apartment'),
    path('Apartamento/Propietario/', views.owner_apartment, name='Owner_apartment'),
    path('Apartamento/Propietario/<int:id_apartamento>/', views.owner_apartment_info, name='Owner_apartment_info'),
    path('Apartamento/Admin/', views.admin_apartment, name='Admin_apartment'),
    path('Apartamento/Admin/<int:id_apartamento>/', views.admin_apartment_info, name='Admin_apartment_info'),
    # ===== ASAMBLEAS =====
    path('asambleas/', views.listar_asambleas, name='listar_asambleas'),
    path('asambleas/crear/', views.crear_asamblea, name='crear_asamblea'),
    path('asambleas/<int:asamblea_id>/', views.detalle_asamblea, name='detalle_asamblea'),
    path('asambleas/<int:asamblea_id>/participantes/', views.participantes_asamblea, name='participantes_asamblea'),

    # ===== PETICIONES =====
    path('peticiones/', views.listar_peticiones, name='listar_peticiones'),
    path('peticiones/crear/', views.crear_peticion, name='crear_peticion'),
    
    # ===== DELEGADOS =====
    path('delegados/', views.crear_delegado, name='crear_delegado'),
    path('delegados/listar/', views.listar_delegados, name='listar_delegados'),
]

