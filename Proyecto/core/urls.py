from django.urls import path
from . import views

urlpatterns = [
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