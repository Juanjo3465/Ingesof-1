from django.shortcuts import render

from django.http import HttpResponse
# core/views.py
from .models import Usuario 

# 2. Define la función de la vista
def listar_usuarios(request):
    # 3. Usa el ORM de Django para pedir todos los objetos del modelo Usuario
    #    Esto se traduce a un "SELECT * FROM Usuario;" en SQL.
    todos_los_usuarios = Usuario.objects.all()

    # 4. Define un "contexto", que es un diccionario para pasar datos a la plantilla
    contexto = {
        'usuarios': todos_los_usuarios
    }

    # 5. Renderiza (dibuja) la plantilla HTML y le pasa el contexto
    return render(request, 'core/listar_usuarios.html', contexto)

def hola(request):
    return HttpResponse("Hola Django, la app core está funcionando ✅")
# Create your views here.
