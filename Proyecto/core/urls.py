from django.urls import path
from . import views

urlpatterns = [
    path('Usuarios/', views.listar_usuarios, name='lista_de_usuarios'),
    path('Header_usuario/', views.header_user, name='Header_user'),
    path('Login/', views.login_view, name='Login'),
    path('Login/Confirmar_usuario/', views.confirm_user, name='Confirm_user'),
    path('Recuperar_contraseña/', views.enter_code, name='Enter_code')
]