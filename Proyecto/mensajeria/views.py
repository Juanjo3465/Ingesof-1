"""Vistas del sistema de mensajería"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from core.services.decorators import login_required
from .services import MensajeriaService


@login_required
def bandeja(request):
    """Vista de la bandeja de entrada/enviados/destacados"""
    service = MensajeriaService()
    usuario = service.get_usuario(request)
    
    tab = request.GET.get('tab', 'recibidos')
    busqueda = request.GET.get('busqueda', '')
    
    if busqueda:
        lista_mensajes = service.buscar_mensajes(usuario, busqueda, tab)
    else:
        if tab == 'enviados':
            lista_mensajes = service.obtener_mensajes_enviados(usuario)
        elif tab == 'destacados':
            lista_mensajes = service.obtener_mensajes_destacados(usuario)
        else:
            lista_mensajes = service.obtener_mensajes_recibidos(usuario)

    mensajes_data = []
    for m in lista_mensajes:
        mensaje = m.id_mensaje
        emisor = service.obtener_emisor(mensaje)
        mensajes_data.append({
            'id': mensaje.id_mensaje,
            'asunto': mensaje.asunto,
            'categoria': mensaje.categoria,
            'fecha': mensaje.fecha_hora,
            'emisor': emisor.nombre if emisor else 'Desconocido',
            'emisor_correo': emisor.correo if emisor else '',
            'leido': m.leido,
            'destacado': m.destacado,
            'papel': m.papel,
        })
    
    no_leidos = service.contar_no_leidos(usuario)
    
    context = {
        'mensajes': mensajes_data,
        'tab_activo': tab,
        'busqueda': busqueda,
        'no_leidos': no_leidos,
    }
    
    return render(request, 'mensajeria/bandeja.html', context)


@login_required
def ver_mensaje(request, mensaje_id):
    """Vista para ver un mensaje específico"""
    service = MensajeriaService()
    usuario = service.get_usuario(request)
    
    usuario_mensaje = service.obtener_mensaje(mensaje_id, usuario)
    
    if usuario_mensaje is None:
        messages.error(request, 'Mensaje no encontrado')
        return redirect('mensajeria:bandeja')
    
    mensaje = usuario_mensaje.id_mensaje

    service.marcar_como_leido(mensaje_id, usuario)

    emisor = service.obtener_emisor(mensaje)
    receptores = service.obtener_receptores(mensaje)

    conversacion = service.obtener_conversacion(mensaje.conversacion, usuario)

    conversacion_data = []
    for msg in conversacion:
        msg_emisor = service.obtener_emisor(msg)
        conversacion_data.append({
            'id': msg.id_mensaje,
            'descripcion': msg.descripcion,
            'fecha': msg.fecha_hora,
            'emisor': msg_emisor.nombre if msg_emisor else 'Desconocido',
            'es_mio': msg_emisor and msg_emisor.id_usuario == usuario.id_usuario,
        })
    
    context = {
        'mensaje': mensaje,
        'emisor': emisor,
        'receptores': receptores,
        'destacado': usuario_mensaje.destacado,
        'conversacion': conversacion_data,
        'es_emisor': usuario_mensaje.papel == 'emisor',
    }
    
    return render(request, 'mensajeria/ver_mensaje.html', context)


@login_required
def redactar(request):
    """Vista para redactar un nuevo mensaje"""
    service = MensajeriaService()
    usuario = service.get_usuario(request)
    
    destinatario_inicial = request.GET.get('para', '')
    respuesta_a = request.GET.get('respuesta_a', '')
    asunto_inicial = request.GET.get('asunto', '')
    
    if request.method == 'POST':
        destinatarios = request.POST.get('destinatarios', '')
        categoria = request.POST.get('categoria', 'General')
        asunto = request.POST.get('asunto', '')
        descripcion = request.POST.get('descripcion', '')
        conversacion_id = request.POST.get('conversacion_id', None)

        if destinatarios == '':
            messages.error(request, 'Debe especificar al menos un destinatario')
        elif asunto == '':
            messages.error(request, 'El asunto es obligatorio')
        elif descripcion == '':
            messages.error(request, 'La descripción es obligatoria')
        else:
            if conversacion_id:
                conversacion_id = int(conversacion_id)
            
            error = service.enviar_mensaje(
                emisor=usuario,
                destinatarios_str=destinatarios,
                categoria=categoria,
                asunto=asunto,
                descripcion=descripcion,
                conversacion_id=conversacion_id
            )
            
            if error:
                messages.error(request, error)
            else:
                messages.success(request, 'Mensaje enviado correctamente')
                return redirect('mensajeria:bandeja')
    
    categorias = ['General', 'Administración', 'Urgente', 'Quejas']
    
    context = {
        'categorias': categorias,
        'destinatario_inicial': destinatario_inicial,
        'asunto_inicial': asunto_inicial,
        'respuesta_a': respuesta_a,
    }
    
    return render(request, 'mensajeria/redactar.html', context)

@login_required
def responder(request, mensaje_id):
    """Vista para responder a un mensaje"""
    service = MensajeriaService()
    usuario = service.get_usuario(request)
    
    usuario_mensaje = service.obtener_mensaje(mensaje_id, usuario)
    
    if not usuario_mensaje:
        messages.error(request, 'Mensaje no encontrado')
        return redirect('mensajeria:bandeja')
    
    mensaje = usuario_mensaje.id_mensaje
    emisor_original = service.obtener_emisor(mensaje)
    
    asunto_original = mensaje.asunto
    if not asunto_original.startswith('Re:'):
        asunto_respuesta = f"Re: {asunto_original}"
    else:
        asunto_respuesta = asunto_original
    
    return redirect(
        f"/mensajeria/redactar/?para={emisor_original.correo}&asunto={asunto_respuesta}&respuesta_a={mensaje.conversacion}"
    )


@login_required
def toggle_destacado(request, mensaje_id):
    """Alterna el estado de destacado de un mensaje"""
    if request.method == 'POST':
        service = MensajeriaService()
        usuario = service.get_usuario(request)
        
        nuevo_estado = service.toggle_destacado(mensaje_id, usuario)
        
        if nuevo_estado is not None:
            return JsonResponse({'destacado': nuevo_estado})
        else:
            return JsonResponse({'error': 'Mensaje no encontrado'}, status=404)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def marcar_leido(request, mensaje_id):
    """Marca un mensaje como leído"""
    if request.method == 'POST':
        service = MensajeriaService()
        usuario = service.get_usuario(request)
        
        exito = service.marcar_como_leido(mensaje_id, usuario)
        
        if exito:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Mensaje no encontrado'}, status=404)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)