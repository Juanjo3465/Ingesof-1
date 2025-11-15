from django.shortcuts import render, redirect

from .models import Reserva, ZonaComun
from core.models import Usuario
from django.contrib import messages
from datetime import datetime, timedelta, time
from itertools import product,chain
from django.utils import timezone

def listar_reservas(request):
    todas_las_reservas = Reserva.objects.all()
    contexto = {
        'reservas': todas_las_reservas
    }
    return render(request, 'reservas/listar_reservas.html', contexto)

# reservas/views.py

#-------------------------------------

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

    campos_ingresados = {
        'id_zona_comun' : id_zona_comun,
        'fecha_reserva_completa' : fecha_hora_a_reservar 
    }
    return campos_ingresados

def reserva_existe(request,campos_ingresados):
    existe = Reserva.objects.filter(
            id_zona_comun_id=campos_ingresados['id_zona_comun'],
            fecha_hora=campos_ingresados['fecha_reserva_completa']
        ).exists()
    return existe

def crear_reserva_view(request):
    if request.method == 'GET':
        zonas_disponibles = ZonaComun.objects.all()
        contexto = {
            'zonas': zonas_disponibles
        }
        return render(request, 'reservas/crear_reservas.html', contexto)
    
    if request.method == 'POST':
        duracion_reserva = 2
        campos_ingresados = obtener_campos(request)
        if campos_ingresados is None:
            return redirect('crear_reserva')
        
        reserva_existente = reserva_existe(request,campos_ingresados)
        
        if reserva_existente:
            messages.error(request, 'Lo sentimos, este horario ya no está disponible. Por favor, elija otro.')
            return redirect('crear_reserva')
        else:
            try:
                usuario_actual = Usuario.objects.get(pk=1) 
                zona_comun_obj = ZonaComun.objects.get(pk=campos_ingresados['id_zona_comun'])
            except (Usuario.DoesNotExist, ZonaComun.DoesNotExist):
                messages.error(request, 'El usuario o la zona común seleccionada no son válidos.')
                return redirect('crear_reserva')

            Reserva.objects.create(
                id_zona_comun=zona_comun_obj,
                id_usuario=usuario_actual,
                fecha_hora=campos_ingresados['fecha_reserva_completa'], 
                cantidad_personas=zona_comun_obj.capacidad,
                duracion = duracion_reserva, 
                costo = zona_comun_obj.costo,
                estado='Confirmada'
            )
            
            messages.success(request, f'¡Reserva para {zona_comun_obj.nombre} confirmada con éxito!')
            return redirect('lista_de_reservas')

#----------------------------

def horarios_posibles_hoy(zonas,ahora,bloques_horarios):
    
    bloques_hoy = []
    
    for bloque in bloques_horarios:
        fecha_naive = datetime.combine(ahora.date(),bloque)
        fecha_aware = timezone.make_aware(fecha_naive)
        if(fecha_aware > ahora):
            bloques_hoy.append(bloque)
    
    horarios_hoy = product([ahora.date()],zonas,bloques_hoy)
            
    return horarios_hoy
    
def horarios_posibles_futuros(zonas,ahora,bloques_horarios):
    dias_semana = 7
    dias_futuros = [ahora.date()+ timedelta(days = i) for i in range(1,dias_semana)]
    combinacion_futuro =  product(dias_futuros,zonas,bloques_horarios)
    return combinacion_futuro
    
def contruir_todos_horarios(request,zonas_procesar):
    
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

def obtener_horarios_ocupados(request,zona_filtrada_id):
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

def reservar_menu_disponible(request):
    
    horarios_seleccionados = request.POST.getlist('horarios_seleccionados')

    if not horarios_seleccionados:
        messages.warning(request, 'Por favor, seleccione al menos un horario para confirmar.')
        return redirect('horarios_disponibles')

    reservas_creadas_count = 0
    for slot in horarios_seleccionados:
        try:
            
            zona_id_str, fecha_hora_str = slot.split('_', 1)
            zona_id = int(zona_id_str)
            fecha_hora = datetime.fromisoformat(fecha_hora_str)
            
            Reserva.objects.create(
                id_zona_comun_id=zona_id,
                id_usuario_id=1, 
                fecha_hora=fecha_hora,
                cantidad_personas = 16,
                estado='Confirmada',
                duracion=2,
                costo=0
            )
            reservas_creadas_count += 1
            
        except (ValueError, IndexError):
            continue

    if reservas_creadas_count > 0:
        messages.success(request, f'¡Se han confirmado {reservas_creadas_count} nueva(s) reserva(s) con éxito!')
    
    return redirect('lista_de_reservas')


def horarios_disponibles_view(request):
    
    if request.method == 'POST':
        return reservar_menu_disponible(request)
    
    zona_filtrada_id = request.GET.get('zona_id')
    
    if zona_filtrada_id:
        zonas_procesar = ZonaComun.objects.filter(pk = zona_filtrada_id)
    else:
        zonas_procesar = ZonaComun.objects.all()
        
    horarios_todos = contruir_todos_horarios(request,zonas_procesar)
    horarios_ocupados = obtener_horarios_ocupados(request,zona_filtrada_id)
    horarios_disponibles = []
    for horario in horarios_todos:
        tupla_horario = (horario['zona_comun'].pk, horario['fecha_hora'])
        if tupla_horario not in horarios_ocupados:
            horarios_disponibles.append(horario)

    contexto = {
        'horarios_disponibles': horarios_disponibles,
        'todas_las_zonas': ZonaComun.objects.all(), 
        'zona_filtrada_id': zona_filtrada_id
    }

    return render(request, 'reservas/horarios_disponibles.html', contexto)