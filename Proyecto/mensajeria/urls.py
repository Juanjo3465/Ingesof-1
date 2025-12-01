"""URLs del sistema de mensajería"""
from django.urls import path
from . import views

app_name = 'mensajeria'

urlpatterns = [
    path('', views.bandeja, name='bandeja'),
    path('mensaje/<int:mensaje_id>/', views.ver_mensaje, name='ver_mensaje'),
    path('redactar/', views.redactar, name='redactar'),
    path('responder/<int:mensaje_id>/', views.responder, name='responder'),
    path('toggle-destacado/<int:mensaje_id>/', views.toggle_destacado, name='toggle_destacado'),
    path('marcar-leido/<int:mensaje_id>/', views.marcar_leido, name='marcar_leido'),
]
