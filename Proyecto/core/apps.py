from django.apps import AppConfig


class AsambleasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asambleas'
    verbose_name = 'Gestión de Asambleas'

"""
Aplicación de gestión de asambleas para MyBuildingApp.

Esta aplicación maneja:
- Creación y gestión de asambleas
- Registro de propietarios y participantes
- Gestión de peticiones
- Control de delegados
"""

default_app_config = 'asambleas.apps.AsambleasConfig'

