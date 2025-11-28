from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from core.services.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Usuario
from .models import Reserva, ZonaComun
from .services import crear_reservas_service
from .services import disponibilidad_service

num_maximo_reservas_activas = 10
def obtener_usuario(request):
    nombre_usuario = request.user.username
    try: 
        usuario_completo = Usuario.objects.get(correo = nombre_usuario)
        return usuario_completo
    except ObjectDoesNotExist:
        print("No se encontro el usuario")
        return None

def obtener_rol(request):
    rol_obj = getattr(request.user, 'role', None)
    rol_usuario = rol_obj.get_name() if rol_obj else 'Usuario'
    return rol_usuario

#Renderizar el menu de reservas
@login_required
def menu_reservas_view(request):
    rol_obj = getattr(request.user, 'role', None)
    rol_usuario = rol_obj.get_name() if rol_obj else 'Usuario'
    contexto = {
        'rol_usuario': rol_usuario
    }
    return render(request,'reservas/menu_reservas.html',contexto)

#Renderiza el template de listar_reservas
@login_required
def listar_reservas(request):
    
    usuario_completo = obtener_usuario(request)
    id_usuario_actual = usuario_completo.pk
    
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
    
    reservas_usuario = Reserva.objects.filter(
        id_usuario = id_usuario_actual,
        fecha_hora__gte = timezone.now()
        ).order_by('fecha_hora')
    print(f"El role es :{request.user.role.get_name()}")
    print(request.user.username)
    rol_obj = getattr(request.user, 'role',None)
    rol_usuario = rol_obj.get_name() if rol_obj else 'Usuario'
    contexto = {
        'reservas' : reservas_usuario,
        'rol_usuario' : rol_usuario
    }
    return render(request,'reservas/mis_reservas.html',contexto)

#Renderiza el template de crear_reservas
@login_required
def crear_reserva_view(request):

    usuario_actual = obtener_usuario(request)
    id_usuario_actual = usuario_actual.pk
    rol_obj = getattr(request.user,'role',None)
    rol_usuario = rol_obj.get_name() if rol_obj else 'Usuario'
    if request.method == 'GET':
        zonas_disponibles = ZonaComun.objects.all()
        contexto = {
            'zonas': zonas_disponibles,
            'rol_usuario' : rol_usuario
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
        
        if not crear_reservas_service.valida_limite_reservas_activas(id_usuario_actual,num_maximo_reservas_activas):
            messages.error(request, 'Has alcanzado el limite maximo de reservaciones')
            return redirect('crear_reserva')
        
        try:
            usuario_actual = Usuario.objects.get(pk=id_usuario_actual)
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
@login_required
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

    role_obj = getattr(request.user, 'role', None)
    rol_nombre = role_obj.get_name() if role_obj else 'Usuario'
    
    contexto = {
        'horarios_disponibles': horarios_disponibles,
        'todas_las_zonas': ZonaComun.objects.all(),
        'rol_usuario' : rol_nombre
    }

    return render(request, 'reservas/horarios_disponibles.html', contexto)

#Gestiona la peticion POST en el template de horarios_disponibles
def reservar_desde_menu_disponible(request):

    usuario_actual = obtener_usuario(request)
    id_usuario_actual = usuario_actual.pk
    horarios_seleccionados = request.POST.getlist('horarios_seleccionados')

    if not horarios_seleccionados:
        messages.warning(request, 'Por favor, seleccione al menos un horario para confirmar.')
        return redirect('horarios_disponibles')

    num_reservas_esperadas = 0
    reservas_creadas_count = 0
    
    for _ in horarios_seleccionados:
        num_reservas_esperadas += 1
        
    if(crear_reservas_service.contar_numero_reservas_activas(id_usuario_actual)+num_reservas_esperadas <= num_maximo_reservas_activas):
        
        for slot in horarios_seleccionados:
            try:
                zona_id_str, fecha_hora_str = slot.split('_', 1)
                zona_id = int(zona_id_str)
                fecha_hora = datetime.fromisoformat(fecha_hora_str)

                Reserva.objects.create(
                    id_zona_comun_id=zona_id,
                    id_usuario_id=id_usuario_actual,
                    fecha_hora=fecha_hora,
                    cantidad_personas = 16,
                    estado='Confirmada',
                    duracion=2,
                    costo=0
                )
                reservas_creadas_count += 1
            except (ValueError, IndexError):
                continue
    elif num_reservas_esperadas == 1:
        messages.error(request,"Has superado el limite maximo de reservaciones activas\n"
                       "Si desea reservar nuevamente, realice una cancelación")
    else:
        messages.error(request,"Ha superado el limite maximo de reservaciones activas."
                       "Verifique reduciendo el numero seleccionado de reservas")
    if reservas_creadas_count > 0:
        messages.success(request, f'¡Se han confirmado {reservas_creadas_count} nueva(s) reserva(s) con éxito!')

    return redirect('lista_de_reservas')
