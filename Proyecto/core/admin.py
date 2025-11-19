"""Configuracion del superusuario admin"""
from django.contrib import admin
from models import Usuario

admin.site.register(Usuario)
