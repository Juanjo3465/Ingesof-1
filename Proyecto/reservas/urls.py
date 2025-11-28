# reservas/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',views.menu_reservas_view, name = 'menu_reservas'),
    path('listar/', views.listar_reservas, name='lista_de_reservas'),
    path('crear/', views.crear_reserva_view, name='crear_reserva'),
    path('disponibles/', views.horarios_disponibles_view, name='horarios_disponibles'),
]
