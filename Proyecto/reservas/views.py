from django.shortcuts import render, redirect

from .models import Reserva, ZonaComun
from core.models import Usuario

def listar_reservas(request):
    todas_las_reservas = Reserva.objects.all()
    contexto = {
        'reservas': todas_las_reservas
    }
    return render(request, 'reservas/listar_reservas.html', contexto)

def crear_reserva_view(request):
    if request.method == 'POST':
        
        zona_comun_id = request.POST.get('zona_comun')
        fecha_reserva_str = request.POST.get('fecha_reserva')
        hora_reserva_str = request.POST.get('hora_reserva')

        try:
            usuario_actual = Usuario.objects.get(pk=1)
        except Usuario.DoesNotExist:
            return redirect('crear_reserva')
        
        zona_comun_obj = ZonaComun.objects.get(pk=zona_comun_id)
        
        fecha_hora_completa = f"{fecha_reserva_str} {hora_reserva_str}"

        Reserva.objects.create(
            id_zona_comun=zona_comun_obj,
            id_usuario=usuario_actual,
            fecha_hora=fecha_hora_completa,
            cantidad_personas=zona_comun_obj.capacidad,
            duracion=2, # en horas
            costo=0.00,
            estado='Confirmada'
        )

        return redirect('lista_de_reservas')

    else:
        zonas_disponibles = ZonaComun.objects.all()
        contexto = {
            'zonas': zonas_disponibles
        }
        return render(request, 'reservas/crear_reservas.html', contexto)