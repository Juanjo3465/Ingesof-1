"""Urls del proyecto principal"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('forum/', include('forum.urls')),
    path('reservas/', include('reservas.urls')),
    path('mensajeria/', include('mensajeria.urls')),
]
