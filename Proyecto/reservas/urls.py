# reservas/urls.py

from django.urls import path
from . import views 

urlpatterns = [
    path('listar/', views.listar_reservas, name='lista_de_reservas'),
    path('crear/', views.crear_reserva_view, name='crear_reserva'),
]