"""Configuracion del superusuario admin"""
from django.contrib import admin
from core.models import Usuario

admin.site.register(Usuario)
