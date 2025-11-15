from itertools import product,chain
from datetime import datetime, timedelta, time
from django.utils import timezone
from ..models import Reserva

def horarios_posibles_hoy(zonas,ahora,bloques_horarios):
    bloques_hoy = []
    for bloque in bloques_horarios:
        fecha_naive = datetime.combine(ahora.date(),bloque)
        fecha_aware = timezone.make_aware(fecha_naive)
        if fecha_aware > ahora:
            bloques_hoy.append(bloque)
    horarios_hoy = product([ahora.date()],zonas,bloques_hoy)
    return horarios_hoy

def horarios_posibles_futuros(zonas,ahora,bloques_horarios):
    dias_semana = 7
    dias_futuros = [ahora.date()+ timedelta(days = i) for i in range(1,dias_semana)]
    combinacion_futuro =  product(dias_futuros,zonas,bloques_horarios)
    return combinacion_futuro

def contruir_todos_horarios_posibles(zonas_procesar):
    bloques_horarios = [time(6,0), time(8,0), time(10,0), time(12,0), time(14,0),
                        time(16,0), time(18,0)]
    ahora_local = timezone.now()
    combinaciones_hoy = horarios_posibles_hoy(zonas_procesar,ahora_local,bloques_horarios)
    combinaciones_futuro = horarios_posibles_futuros(zonas_procesar,ahora_local,bloques_horarios)
    todas_combinaciones = chain(combinaciones_hoy, combinaciones_futuro)
    posibles_reservas = []
    for fecha,zona,bloque in todas_combinaciones:
        nuevo_hueco = {
        'zona_comun': zona,
        'fecha_hora': timezone.make_aware(datetime.combine(fecha, bloque))
        }
        posibles_reservas.append(nuevo_hueco)
    return posibles_reservas

def obtener_horarios_ocupados(zona_filtrada_id):
    reservas_ocupadas = Reserva.objects.filter(
        fecha_hora__gte=timezone.now(),
        estado='Confirmada'
    )
    horarios_ocupados = {}
    if zona_filtrada_id:
        reservas_ocupadas = reservas_ocupadas.filter(id_zona_comun = zona_filtrada_id)
    horarios_ocupados = {
        (reserva.id_zona_comun.pk, reserva.fecha_hora) for reserva in reservas_ocupadas
    }
    return horarios_ocupados

def construir_reservas_disponibles(horarios_todos,horarios_ocupados):
    horarios_disponibles = []
    for horario in horarios_todos:
        tupla_horario = (horario['zona_comun'].pk, horario['fecha_hora'])
        if tupla_horario not in horarios_ocupados:
            horarios_disponibles.append(horario)
    return horarios_disponibles
