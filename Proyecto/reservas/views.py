from django.shortcuts import render

from .models import Reserva

def listar_reservas(request):
    todas_las_reservas = Reserva.objects.all()
    contexto = {
        'reservas': todas_las_reservas
    }
    return render(request, 'reservas/listar_reservas.html', contexto)
