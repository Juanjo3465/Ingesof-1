from django.urls import path
from . import views

urlpatterns = [
    # ===== ASAMBLEAS =====
    # Listar todas
    path('api/asambleas', views.listar_asambleas, name='listar_asambleas'),
    # Crear nueva
    path('api/asambleas/', views.crear_asamblea, name='crear_asamblea'),
    # Detalle de una asamblea
    path('api/asambleas/<int:asamblea_id>', views.detalle_asamblea, name='detalle_asamblea'),
    # Participantes de una asamblea
    path('api/asambleas/<int:asamblea_id>/participantes', views.participantes_asamblea, name='participantes_asamblea'),

    # ===== PETICIONES =====
    # Listar todas
    path('api/peticiones', views.listar_peticiones, name='listar_peticiones'),
    # Crear nueva
    path('api/peticiones/', views.crear_peticion, name='crear_peticion'),
]
