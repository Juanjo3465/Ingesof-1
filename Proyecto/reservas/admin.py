from django.contrib import admin

# Register your models here.
from .models import ZonaComun, Reserva

# Registramos ambos modelos para que aparezcan en el panel de administración
admin.site.register(ZonaComun)
admin.site.register(Reserva)
