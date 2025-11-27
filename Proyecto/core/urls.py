"""Urls del core del proyecto"""
from django.urls import path
from core.views import views

urlpatterns = [
    path('Usuarios/', views.listar_usuarios, name='lista_de_usuarios'),
    path('', views.inicial_page, name='Inicial_page'),
    path('Header_usuario/', views.header_user, name='Header_user'),
    path('Login/', views.login_view, name='Login'),
    path('Login/Confirmar_usuario/', views.confirm_user, name='Confirm_user'),
    path('Recuperar_contraseña/', views.enter_code, name='Enter_code'),
    path('Cambiar_contraseña/', views.change_password, name='Change_pass')
]
