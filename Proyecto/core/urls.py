"""Urls del core del proyecto"""
from django.urls import path
from core.views import views, verify_session
from core import views_asamblea

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
    # ========== Vistas de Templates ==========
    path('crear/', views_asamblea.vista_crear_asamblea, name='crear_asamblea'),
    path('consultar/', views_asamblea.vista_consultar_asambleas, name='consultar_asambleas'),
    path('delegar/', views_asamblea.vista_delegar, name='delegar'),
    path('peticion/', views_asamblea.vista_crear_peticion, name='crear_peticion'),
    
    # ========== API Asambleas ==========
    path('api/asambleas/', views_asamblea.listar_asambleas, name='api_listar_asambleas'),
    path('api/asambleas/crear/', views_asamblea.crear_asamblea, name='api_crear_asamblea'),
    path('api/asambleas/<int:asamblea_id>/', views_asamblea.detalle_asamblea, name='api_detalle_asamblea'),
    path('api/asambleas/<int:asamblea_id>/participantes/', views_asamblea.participantes_asamblea, name='api_participantes_asamblea'),
    
    # ========== API Delegados ==========
    path('api/delegados/', views_asamblea.listar_delegados, name='api_listar_delegados'),
    path('api/delegados/crear/', views_asamblea.crear_delegado, name='api_crear_delegado'),
    
    # ========== API Peticiones ==========
    path('api/peticiones/', views_asamblea.listar_peticiones, name='api_listar_peticiones'),
    path('api/peticiones/crear/', views_asamblea.crear_peticion, name='api_crear_peticion'),
]
