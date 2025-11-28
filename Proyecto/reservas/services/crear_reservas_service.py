from datetime import datetime, time, timedelta
from django.utils import timezone
from django.contrib import messages
from ..models import Reserva

def obtener_campos(request):
    id_zona_comun = request.POST.get('zona_comun')
    fecha_reserva_str = request.POST.get('fecha_reserva')
    hora_reserva_str = request.POST.get('hora_reserva')

    try:
        fecha_obj = datetime.strptime(fecha_reserva_str, '%Y-%m-%d').date()
        hora_obj = time.fromisoformat(hora_reserva_str)
        fecha_hora_ingenua = datetime.combine(fecha_obj, hora_obj)
        fecha_hora_a_reservar = timezone.make_aware(fecha_hora_ingenua)

    except (ValueError, TypeError):
        messages.error(request, 'El formato de fecha u hora es inválido.')
        return None

    try:
        int(id_zona_comun)

    except ValueError:
        messages.error(request, 'El formato de para elegir la zona comun no es valido')
        return None

    campos_ingresados = {
        'id_zona_comun' : id_zona_comun,
        'fecha_reserva_completa' : fecha_hora_a_reservar 
    }
    return campos_ingresados

def reserva_existe(campos_ingresados):
    existe = Reserva.objects.filter(
            id_zona_comun_id=campos_ingresados['id_zona_comun'],
            fecha_hora=campos_ingresados['fecha_reserva_completa']
        ).exists()
    return existe

def valida_reserva_posterior_ahora(campos_ingresados):
    
    dia_hora_reserva = campos_ingresados['fecha_reserva_completa']
    ahora_local = timezone.now()
    if dia_hora_reserva > ahora_local:
        return True
    return False

def valida_alcance_reserva(campos_ingresados):
    
    dia_hora_reserva = campos_ingresados['fecha_reserva_completa']
    dias_max_prev_reservar = 180
    fecha_limite_reserva = timezone.now() + timedelta(days=dias_max_prev_reservar)
    
    if dia_hora_reserva > fecha_limite_reserva:
        return False
    
    return True
    
    
    
