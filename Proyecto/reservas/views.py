from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Usuario
from .models import Reserva, ZonaComun
from .services import crear_reservas_service
from .services import disponibilidad_service

#Renderizar el menu de reservas
def menu_reservas_view(request):
    contexto = {}
    return render(request,'reservas/menu_reservas.html',contexto)

#Renderiza el template de mis reservas
def listar_reservas(request):
    id_usuario_actual = 1
    
    if request.method == 'POST':
        lista_cancelaciones = request.POST.getlist('reservas_a_cancelar')
        
        if not lista_cancelaciones:
            messages.warning(request,'No ha seleccionado ninguna reserva para cancelar')
        else:
            lista_reservas_borrar =  Reserva.objects.filter(
                pk__in = lista_cancelaciones,
                id_usuario = id_usuario_actual
            )
            cantidad_borrar = lista_reservas_borrar.count()
            
            if cantidad_borrar > 0:
                lista_reservas_borrar.delete()
                messages.success(request, f'Se han cancelado {cantidad_borrar} reserva(s) con éxito.')
            
        return redirect('lista_de_reservas')
    
    reservas_usuario = Reserva.objects.filter(id_usuario = id_usuario_actual).order_by('fecha_hora')
    contexto = {
        'reservas' : reservas_usuario 
    }
    return render(request,'reservas/mis_reservas.html',contexto)

#Renderiza el template de crear_reservas
def crear_reserva_view(request):

    if request.method == 'GET':
        zonas_disponibles = ZonaComun.objects.all()
        contexto = {
            'zonas': zonas_disponibles
        }
        return render(request, 'reservas/crear_reservas.html', contexto)

    if request.method == 'POST':
        duracion_reserva = 2
        campos_ingresados = crear_reservas_service.obtener_campos(request)
        if campos_ingresados is None:
            return redirect('crear_reserva')

        reserva_existente = crear_reservas_service.reserva_existe(campos_ingresados)

        if reserva_existente:
            messages.error(request, 'Lo sentimos, este horario ya no está disponible. Por favor, elija otro.')
            return redirect('crear_reserva')

        if not crear_reservas_service.valida_reserva_posterior_ahora(campos_ingresados):
            messages.error(request, 'No se pueden hacer reservaciones en horarios previos a la fecha actual')
            return redirect('crear_reserva')
        
        if not crear_reservas_service.valida_alcance_reserva(campos_ingresados):
            messages.error(request, 'No se pueden agenda reservas en un rango superior a 6 meses')
            return redirect('crear_reserva')
        
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

#Renderiza el template de horarios_disponibles

def horarios_disponibles_view(request):

    if request.method == 'POST':
        return reservar_desde_menu_disponible(request)

    zona_filtrada_id = request.GET.get('zona_id')
    if zona_filtrada_id:
        zonas_procesar = ZonaComun.objects.filter(pk = zona_filtrada_id)
    else:
        zonas_procesar = ZonaComun.objects.all()

    horarios_todos = disponibilidad_service.contruir_todos_horarios_posibles(zonas_procesar)
    horarios_ocupados = disponibilidad_service.obtener_horarios_ocupados(zona_filtrada_id)
    horarios_disponibles = disponibilidad_service.construir_reservas_disponibles(horarios_todos,horarios_ocupados)

    contexto = {
        'horarios_disponibles': horarios_disponibles,
        'todas_las_zonas': ZonaComun.objects.all(), 
    }

    return render(request, 'reservas/horarios_disponibles.html', contexto)

#Gestiona la peticion POST en el template de horarios_disponibles
def reservar_desde_menu_disponible(request):

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
