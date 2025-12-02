"""Vistas para el módulo de Asambleas"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
import json

from .models import Asamblea, Delegado, Peticion, Usuario
from .services.decorators import login_required, role_required
from .services.account_service import AccountService


# ========== VISTAS DE RENDERIZADO (Templates) ==========

@login_required
@role_required(Usuario.Rol_Administrador)
def vista_crear_asamblea(request):
    """Renderiza el template para crear asamblea - Solo Administrador"""
    return render(request, 'core/CrearAsamblea.html')


@login_required
def vista_consultar_asambleas(request):
    """Renderiza el template para consultar asambleas"""
    return render(request, 'core/ConsultaAsambleas.html')


@login_required
@role_required(Usuario.Rol_Propietario, Usuario.Rol_Administrador)
def vista_delegar(request):
    """Renderiza el template para delegar - Solo Propietarios"""
    return render(request, 'core/delegar.html')


@login_required
@role_required(Usuario.Rol_Propietario, Usuario.Rol_Administrador)
def vista_crear_peticion(request):
    """Renderiza el template para crear petición - Solo Propietarios"""
    return render(request, 'core/peticion.html')


# ========== API ASAMBLEAS ==========

@require_http_methods(["POST"])
@role_required(Usuario.Rol_Administrador)
def crear_asamblea(request):
    """Crear nueva asamblea - Solo Administrador - Devuelve JSON"""
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
            if 'T' in fecha_hora_str:
                fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
            else:
                fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M:%S')
            
            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora)
                
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'success': False,
                'mensaje': f'Formato de fecha inválido: {str(e)}'
            }, status=400)
        
        # Validar que la fecha sea futura
        if fecha_hora <= timezone.now():
            return JsonResponse({
                'success': False,
                'mensaje': 'La fecha de la asamblea debe ser futura'
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


@require_http_methods(["GET"])
@login_required
def listar_asambleas(request):
    """Listar todas las asambleas - Devuelve JSON"""
    try:
        asambleas = Asamblea.objects.all().order_by('-fecha_hora')
        
        data = [{
            'id_asamblea': a.id_asamblea,
            'nombre': a.nombre,
            'lugar': a.lugar,
            'fecha_hora': a.fecha_hora.strftime('%Y-%m-%d %H:%M:%S') if a.fecha_hora else None,
            'descripcion': a.descripcion,
            'estado': a.estado,
            'doc_convocatoria': bool(a.doc_convocatoria),
            'doc_citacion': bool(a.doc_citacion),
            'acta_asamblea': bool(a.acta_asamblea),
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
@login_required
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
                'fecha_hora': asamblea.fecha_hora.strftime('%Y-%m-%d %H:%M:%S') if asamblea.fecha_hora else None,
                'descripcion': asamblea.descripcion,
                'estado': asamblea.estado,
                'doc_convocatoria': bool(asamblea.doc_convocatoria),
                'doc_citacion': bool(asamblea.doc_citacion),
                'acta_asamblea': bool(asamblea.acta_asamblea),
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al obtener asamblea: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
@login_required
def participantes_asamblea(request, asamblea_id):
    """Obtener participantes (delegados) de una asamblea - Devuelve JSON"""
    try:
        asamblea = get_object_or_404(Asamblea, pk=asamblea_id)
        
        # Obtener delegados de esta asamblea
        delegados = Delegado.objects.filter(
            id_asamblea=asamblea
        ).select_related('id_propietario')
        
        # Estadísticas
        total_propietarios = Usuario.objects.filter(rol=Usuario.Rol_Propietario).count()
        total_delegados = delegados.count()
        
        # Serializar delegados
        delegados_data = [{
            'id': d.id,
            'nombre': d.nombre,
            'cedula': d.cedula,
            'propietario_nombre': d.id_propietario.nombre if d.id_propietario else 'Sin propietario',
            'propietario_cedula': d.id_propietario.cedula if d.id_propietario else None,
        } for d in delegados]
        
        return JsonResponse({
            'success': True,
            'estadisticas': {
                'total_propietarios': total_propietarios,
                'total_delegados': total_delegados,
            },
            'delegados': delegados_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'mensaje': f'Error al obtener participantes: {str(e)}'
        }, status=500)


# ========== API DELEGADOS ==========

@require_http_methods(["POST"])
@role_required(Usuario.Rol_Propietario)
def crear_delegado(request):
    """Crear delegado para una asamblea - Solo Propietarios - Devuelve JSON"""
    try:
        data = json.loads(request.body)
        
        # Obtener el usuario propietario actual
        account_service = AccountService()
        propietario = account_service.get_app_user(request.user)
        
        if not propietario:
            return JsonResponse({
                'success': False,
                'mensaje': 'No se pudo identificar al propietario'
            }, status=400)
        
        # Validaciones
        id_asamblea = data.get('id_asamblea')
        cedula_delegado = data.get('cedula')
        nombre = data.get('nombre', '').strip()
        
        if not id_asamblea:
            return JsonResponse({
                'success': False,
                'mensaje': 'Debe seleccionar una asamblea'
            }, status=400)
        
        # Validar cédula del delegado
        try:
            cedula_delegado = int(cedula_delegado)
            if cedula_delegado <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'mensaje': 'La cédula del delegado debe ser un número válido'
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
        
        # Verificar que la asamblea esté programada y sea futura
        if asamblea.estado != 'Programada':
            return JsonResponse({
                'success': False,
                'mensaje': 'Solo puede delegar en asambleas programadas'
            }, status=400)
        
        if asamblea.fecha_hora and asamblea.fecha_hora <= timezone.now():
            return JsonResponse({
                'success': False,
                'mensaje': 'No puede delegar en asambleas pasadas'
            }, status=400)
        
        # Verificar que no exista ya un delegado para este propietario en esta asamblea
        delegado_existente = Delegado.objects.filter(
            id_propietario=propietario,
            id_asamblea=asamblea
        ).exists()
        
        if delegado_existente:
            return JsonResponse({
                'success': False,
                'mensaje': 'Ya tiene un delegado registrado para esta asamblea'
            }, status=400)
        
        # Crear delegado
        delegado = Delegado.objects.create(
            id_propietario=propietario,
            id_asamblea=asamblea,
            cedula=cedula_delegado,
            nombre=nombre
        )
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Delegado registrado exitosamente',
            'data': {
                'id': delegado.id,
                'nombre': delegado.nombre,
                'cedula': delegado.cedula,
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
@login_required
def listar_delegados(request):
    """Listar delegados del usuario actual - Devuelve JSON"""
    try:
        account_service = AccountService()
        usuario = account_service.get_app_user(request.user)
        
        # Si es administrador, muestra todos los delegados
        if usuario and usuario.rol == Usuario.Rol_Administrador:
            delegados = Delegado.objects.select_related(
                'id_asamblea', 'id_propietario'
            ).all().order_by('-id_asamblea__fecha_hora')
        else:
            # Si es propietario, solo sus delegados
            delegados = Delegado.objects.filter(
                id_propietario=usuario
            ).select_related('id_asamblea').order_by('-id_asamblea__fecha_hora')
        
        data = [{
            'id': d.id,
            'nombre': d.nombre,
            'cedula': d.cedula,
            'propietario_nombre': d.id_propietario.nombre if d.id_propietario else 'N/A',
            'asamblea_nombre': d.id_asamblea.nombre if d.id_asamblea else 'N/A',
            'fecha_asamblea': d.id_asamblea.fecha_hora.strftime('%Y-%m-%d %H:%M:%S') if d.id_asamblea and d.id_asamblea.fecha_hora else None,
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


# ========== API PETICIONES ==========

@require_http_methods(["POST"])
@role_required(Usuario.Rol_Propietario)
def crear_peticion(request):
    """Crear nueva petición - Solo Propietarios - Devuelve JSON"""
    try:
        data = json.loads(request.body)
        
        # Obtener el usuario propietario actual
        account_service = AccountService()
        propietario = account_service.get_app_user(request.user)
        
        if not propietario:
            return JsonResponse({
                'success': False,
                'mensaje': 'No se pudo identificar al propietario'
            }, status=400)
        
        # Validaciones
        asunto = data.get('asunto', '').strip()
        descripcion = data.get('descripcion', '').strip()
        id_asamblea = data.get('id_asamblea')
        
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
        
        # Crear petición
        peticion = Peticion.objects.create(
            id_asamblea=asamblea,
            id_propietario=propietario,
            asunto=asunto,
            descripcion=descripcion,
            fecha_peticion=timezone.now(),
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
@login_required
def listar_peticiones(request):
    """Listar peticiones - Devuelve JSON"""
    try:
        account_service = AccountService()
        usuario = account_service.get_app_user(request.user)
        
        # Si es administrador, muestra todas las peticiones
        if usuario and usuario.rol == Usuario.Rol_Administrador:
            peticiones = Peticion.objects.select_related(
                'id_propietario', 'id_asamblea'
            ).all().order_by('-fecha_peticion')
        else:
            # Si es propietario, solo sus peticiones
            peticiones = Peticion.objects.filter(
                id_propietario=usuario
            ).select_related('id_asamblea').order_by('-fecha_peticion')
        
        data = [{
            'id_peticion': p.id_peticion,
            'asunto': p.asunto,
            'descripcion': p.descripcion,
            'estado': p.estado,
            'propietario_nombre': p.id_propietario.nombre if p.id_propietario else 'Sin propietario',
            'asamblea_nombre': p.id_asamblea.nombre if p.id_asamblea else 'Sin asamblea',
            'fecha_peticion': p.fecha_peticion.strftime('%Y-%m-%d %H:%M:%S') if p.fecha_peticion else None,
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