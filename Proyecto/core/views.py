from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count
from datetime import datetime
import json
from .models import Asamblea, Propietario, ParticipacionAsamblea, Delegado, Peticion


# ========== ASAMBLEAS ==========

@csrf_exempt
@require_http_methods(["POST"])
def crear_asamblea(request):
    """Crear nueva asamblea - Devuelve JSON"""
    try:
        data = json.loads(request.body)
        
        # Validaciones
        nombre = data.get('nombre', '').strip()
        lugar = data.get('lugar', '').strip()
        fecha_hora_str = data.get('fecha_hora')
        descripcion = data.get('descripcion', '').strip()
        
        if len(nombre) < 5:
            return JsonResponse({
                'success': False,
                'mensaje': 'El nombre debe tener al menos 5 caracteres'
            }, status=400)
        
        if len(lugar) < 3:
            return JsonResponse({
                'success': False,
                'mensaje': 'El lugar debe tener al menos 3 caracteres'
            }, status=400)
        
        if len(descripcion) < 20:
            return JsonResponse({
                'success': False,
                'mensaje': 'La descripción debe tener al menos 20 caracteres'
            }, status=400)
        
        # Convertir string de fecha a datetime
        try:
            # El frontend envía formato: "2025-12-15T14:30"
            if 'T' in fecha_hora_str:
                fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
            else:
                fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M:%S')
            
            # Hacer timezone-aware si USE_TZ=True en settings
            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora)
                
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'success': False,
                'mensaje': f'Formato de fecha inválido: {str(e)}'
            }, status=400)
        
        # Crear asamblea
        asamblea = Asamblea.objects.create(
            nombre=nombre,
            lugar=lugar,
            fecha_hora=fecha_hora,
            descripcion=descripcion,
            estado=data.get('estado', 'Programada')
        )
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Asamblea creada exitosamente',
            'data': {
                'id_asamblea': asamblea.id_asamblea,
                'nombre': asamblea.nombre,
                'lugar': asamblea.lugar,
                'fecha_hora': fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                'descripcion': asamblea.descripcion,
                'estado': asamblea.estado
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'mensaje': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al crear la asamblea: {str(e)}'
        }, status=500)
@csrf_exempt
@require_http_methods(["POST"])
def crear_delegado(request):
    """Crear delegado para una asamblea - Devuelve JSON"""
    try:
        data = json.loads(request.body)
        
        # Validaciones
        id_asamblea = data.get('id_asamblea')
        cedula_propietario = data.get('cedula_propietario', '').strip()
        cedula_delegado = data.get('cedula', '').strip()
        nombre = data.get('nombre', '').strip()
        
        if not id_asamblea:
            return JsonResponse({
                'success': False,
                'mensaje': 'Debe seleccionar una asamblea'
            }, status=400)
        
        if not cedula_propietario:
            return JsonResponse({
                'success': False,
                'mensaje': 'La cédula del propietario es requerida'
            }, status=400)
        
        if len(cedula_propietario) < 6 or len(cedula_propietario) > 20:
            return JsonResponse({
                'success': False,
                'mensaje': 'La cédula del propietario debe tener entre 6 y 20 caracteres'
            }, status=400)
        
        if len(cedula_delegado) < 6 or len(cedula_delegado) > 20:
            return JsonResponse({
                'success': False,
                'mensaje': 'La cédula del delegado debe tener entre 6 y 20 caracteres'
            }, status=400)
        
        if len(nombre) < 3:
            return JsonResponse({
                'success': False,
                'mensaje': 'El nombre debe tener al menos 3 caracteres'
            }, status=400)
        
        # Verificar que la asamblea existe
        try:
            asamblea = Asamblea.objects.get(pk=id_asamblea)
        except Asamblea.DoesNotExist:
            return JsonResponse({
                'success': False,
                'mensaje': 'La asamblea no existe'
            }, status=404)
        
        # Verificar que no haya delegado ya para esta asamblea y esta cédula de propietario
        delegado_existente = Delegado.objects.filter(
            asamblea=asamblea,
            cedula_propietario=cedula_propietario
        ).first()
        
        if delegado_existente:
            return JsonResponse({
                'success': False,
                'mensaje': 'Ya existe un delegado registrado para este propietario en esta asamblea'
            }, status=400)
        
        # Crear delegado (sin validar que el propietario exista)
        delegado = Delegado.objects.create(
            asamblea=asamblea,
            cedula_propietario=cedula_propietario,
            nombre_delegado=nombre,
            cedula=cedula_delegado
        )
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Delegado registrado exitosamente',
            'data': {
                'id_delegado': delegado.id_delegado,
                'nombre_delegado': delegado.nombre_delegado,
                'cedula': delegado.cedula,
                'cedula_propietario': delegado.cedula_propietario,
                'asamblea': asamblea.nombre
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'mensaje': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al registrar delegado: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def listar_delegados(request):
    """Listar todos los delegados - Devuelve JSON"""
    try:
        delegados = Delegado.objects.select_related('asamblea').all().order_by('-fecha_registro')
        
        data = [{
            'id_delegado': d.id_delegado,
            'nombre_delegado': d.nombre_delegado,
            'cedula': d.cedula,
            'cedula_propietario': d.cedula_propietario,
            'asamblea': d.asamblea.nombre,
            'fecha_asamblea': d.asamblea.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_registro': d.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
        } for d in delegados]
        
        return JsonResponse({
            'success': True,
            'delegados': data,
            'total': len(data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al listar delegados: {str(e)}'
        }, status=500)
@require_http_methods(["GET"])


def listar_asambleas(request):
    """Listar todas las asambleas - Devuelve JSON"""
    try:
        asambleas = Asamblea.objects.all().order_by('-fecha_hora')
        
        data = [{
            'id_asamblea': a.id_asamblea,
            'nombre': a.nombre,
            'lugar': a.lugar,
            'fecha_hora': a.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            'descripcion': a.descripcion,
            'estado': a.estado,
            'doc_convocatoria': bool(a.doc_convocatoria),
            'doc_citacion': bool(a.doc_citacion),
            'doc_acta': bool(a.doc_acta),
        } for a in asambleas]
        
        return JsonResponse({
            'success': True,
            'asambleas': data,
            'total': len(data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al listar asambleas: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def detalle_asamblea(request, asamblea_id):
    """Obtener detalle de una asamblea - Devuelve JSON"""
    try:
        asamblea = get_object_or_404(Asamblea, pk=asamblea_id)
        
        return JsonResponse({
            'success': True,
            'asamblea': {
                'id_asamblea': asamblea.id_asamblea,
                'nombre': asamblea.nombre,
                'lugar': asamblea.lugar,
                'fecha_hora': asamblea.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
                'descripcion': asamblea.descripcion,
                'estado': asamblea.estado,
                'doc_convocatoria': bool(asamblea.doc_convocatoria),
                'doc_citacion': bool(asamblea.doc_citacion),
                'doc_acta': bool(asamblea.doc_acta),
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al obtener asamblea: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def participantes_asamblea(request, asamblea_id):
    """Obtener participantes de una asamblea con estadísticas - Devuelve JSON"""
    try:
        asamblea = get_object_or_404(Asamblea, pk=asamblea_id)
        
        # Obtener participaciones personales
        participaciones = ParticipacionAsamblea.objects.filter(
            asamblea=asamblea,
            tipo_participacion='Personal'
        ).select_related('propietario')
        
        # Obtener delegados
        delegados = Delegado.objects.filter(
            asamblea=asamblea
        ).select_related('propietario')
        
        # Estadísticas
        total_propietarios = Propietario.objects.count()
        propietarios_presentes = participaciones.count()
        total_delegados = delegados.count()
        total_participantes = propietarios_presentes + total_delegados
        
        # Serializar participaciones
        participaciones_data = [{
            'id_participacion': p.id_participacion,
            'nombre': p.propietario.nombre,
            'apartamentos': p.propietario.apartamentos or 'Sin apartamento',
        } for p in participaciones]
        
        # Serializar delegados
        delegados_data = [{
            'id_delegado': d.id_delegado,
            'nombre_delegado': d.nombre_delegado,
            'cedula': d.cedula,
            'nombre_propietario': d.propietario.nombre,
        } for d in delegados]
        
        return JsonResponse({
            'success': True,
            'estadisticas': {
                'total_propietarios': total_propietarios,
                'propietarios_presentes': propietarios_presentes,
                'total_delegados': total_delegados,
                'total_participantes': total_participantes,
            },
            'propietarios_presentes': participaciones_data,
            'delegados': delegados_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al obtener participantes: {str(e)}'
        }, status=500)


# ========== PETICIONES ==========

@csrf_exempt
@require_http_methods(["POST"])
def crear_peticion(request):
    """Crear nueva petición - Devuelve JSON"""
    try:
        data = json.loads(request.body)
        
        # Validaciones
        asunto = data.get('asunto', '').strip()
        descripcion = data.get('descripcion', '').strip()
        id_asamblea = data.get('id_asamblea')
        id_propietario = data.get('id_propietario')
        
        if len(asunto) < 5:
            return JsonResponse({
                'success': False,
                'mensaje': 'El asunto debe tener al menos 5 caracteres'
            }, status=400)
        
        if len(descripcion) < 20:
            return JsonResponse({
                'success': False,
                'mensaje': 'La descripción debe tener al menos 20 caracteres'
            }, status=400)
        
        # Verificar que la asamblea existe
        try:
            asamblea = Asamblea.objects.get(pk=id_asamblea)
        except Asamblea.DoesNotExist:
            return JsonResponse({
                'success': False,
                'mensaje': 'La asamblea no existe'
            }, status=404)
        
        # Intentar obtener el propietario, pero si no existe, dejarlo en null
        propietario = None
        if id_propietario:
            try:
                propietario = Propietario.objects.get(pk=id_propietario)
            except Propietario.DoesNotExist:
                # Si el propietario no existe, simplemente lo dejamos como null
                propietario = None
        
        # Crear petición
        peticion = Peticion.objects.create(
            asamblea=asamblea,
            propietario=propietario,
            asunto=asunto,
            descripcion=descripcion,
            estado='Pendiente'
        )
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Petición enviada exitosamente',
            'data': {
                'id_peticion': peticion.id_peticion,
                'asunto': peticion.asunto,
                'descripcion': peticion.descripcion,
                'estado': peticion.estado
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'mensaje': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al crear la petición: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def listar_peticiones(request):
    """Listar todas las peticiones - Devuelve JSON"""
    try:
        peticiones = Peticion.objects.select_related(
            'propietario', 'asamblea'
        ).all().order_by('-fecha_creacion')
        
        data = [{
            'id_peticion': p.id_peticion,
            'asunto': p.asunto,
            'descripcion': p.descripcion,
            'estado': p.estado,
            'nombre_propietario': p.propietario.nombre if p.propietario else 'Sin propietario',
            'nombre_asamblea': p.asamblea.nombre,
            'fecha_creacion': p.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
        } for p in peticiones]
        
        return JsonResponse({
            'success': True,
            'peticiones': data,
            'total': len(data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al listar peticiones: {str(e)}'
        }, status=500)