from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.listar_usuarios, name='lista_de_usuarios'),
]