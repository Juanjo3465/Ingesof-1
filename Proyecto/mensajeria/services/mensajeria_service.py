"""Servicios de mensajería"""
from django.utils import timezone
from django.db.models import Q
from core.models import Usuario, Apartamentos
from ..models import Mensaje, UsuarioMensaje
from core.services.account_service import AccountService


class MensajeriaService:
    """Servicio para manejar la lógica de mensajería"""

    def __init__(self):
        self.account_service = AccountService()

    def get_usuario(self, request):
        """Obtiene el usuario de la app desde request"""
        return self.account_service.get_app_user(request.user)

    def obtener_mensajes_recibidos(self, usuario):
        """Obtiene los mensajes donde el usuario es receptor"""
        return UsuarioMensaje.objects.filter(
            id_usuario=usuario,
            papel='receptor'
        ).select_related('id_mensaje').order_by('-id_mensaje__fecha_hora')

    def obtener_mensajes_enviados(self, usuario):
        """Obtiene los mensajes donde el usuario es emisor"""
        return UsuarioMensaje.objects.filter(
            id_usuario=usuario,
            papel='emisor'
        ).select_related('id_mensaje').order_by('-id_mensaje__fecha_hora')

    def obtener_mensajes_destacados(self, usuario):
        """Obtiene los mensajes marcados como destacados"""
        return UsuarioMensaje.objects.filter(
            id_usuario=usuario,
            destacado=1
        ).select_related('id_mensaje').order_by('-id_mensaje__fecha_hora')

    def obtener_mensaje(self, mensaje_id, usuario):
        """Obtiene un mensaje específico si el usuario tiene acceso"""
        try:
            usuario_mensaje = UsuarioMensaje.objects.select_related('id_mensaje').get(
                id_mensaje__id_mensaje=mensaje_id,
                id_usuario=usuario
            )
            return usuario_mensaje
        except UsuarioMensaje.DoesNotExist:
            return None

    def obtener_conversacion(self, conversacion_id, usuario):
        """Obtiene todos los mensajes de una conversación"""
        mensajes_ids = UsuarioMensaje.objects.filter(
            id_usuario=usuario,
            id_mensaje__conversacion=conversacion_id
        ).values_list('id_mensaje', flat=True)
        
        return Mensaje.objects.filter(
            id_mensaje__in=mensajes_ids
        ).order_by('fecha_hora')

    def obtener_emisor(self, mensaje):
        """Obtiene el usuario emisor de un mensaje"""
        try:
            emisor_rel = UsuarioMensaje.objects.select_related('id_usuario').get(
                id_mensaje=mensaje,
                papel='emisor'
            )
            return emisor_rel.id_usuario
        except UsuarioMensaje.DoesNotExist:
            return None

    def obtener_receptores(self, mensaje):
        """Obtiene los usuarios receptores de un mensaje"""
        return UsuarioMensaje.objects.filter(
            id_mensaje=mensaje,
            papel='receptor'
        ).select_related('id_usuario')

    def marcar_como_leido(self, mensaje_id, usuario):
        """Marca un mensaje como leído"""
        try:
            usuario_mensaje = UsuarioMensaje.objects.get(
                id_mensaje__id_mensaje=mensaje_id,
                id_usuario=usuario
            )
            if usuario_mensaje.leido != 1:
                usuario_mensaje.leido = 1
                usuario_mensaje.fecha_lectura = timezone.now()
                usuario_mensaje.save()
            return True
        except UsuarioMensaje.DoesNotExist:
            return False

    def toggle_destacado(self, mensaje_id, usuario):
        """Alterna el estado de destacado de un mensaje"""
        try:
            usuario_mensaje = UsuarioMensaje.objects.get(
                id_mensaje__id_mensaje=mensaje_id,
                id_usuario=usuario
            )
            usuario_mensaje.destacado = 0 if usuario_mensaje.destacado == 1 else 1
            usuario_mensaje.save()
            return usuario_mensaje.destacado
        except UsuarioMensaje.DoesNotExist:
            return None

    def parsear_apartamento(self, texto):
        """
        Parsea el formato de apartamento.
        Formatos válidos:
            - 'interior-torre-numero' (ej: 2-1-301)
            - 'torre-numero' (ej: 1-301) cuando no hay interior
        """
        partes = texto.split('-')
        
        try:
            if len(partes) == 3:
                # Formato: interior-torre-numero
                interior = int(partes[0])
                torre = int(partes[1])
                numero = int(partes[2])
                return (interior, torre, numero)
            elif len(partes) == 2:
                # Formato: torre-numero (sin interior)
                torre = int(partes[0])
                numero = int(partes[1])
                return (None, torre, numero)
        except ValueError:
            pass
        
        return None

    def buscar_apartamento(self, interior, torre, numero):
        """
        Busca un apartamento por sus componentes.
        Retorna el apartamento o None si no existe.
        """
        try:
            if interior is not None:
                return Apartamentos.objects.get(
                    interior=interior,
                    torre=torre,
                    numero=numero
                )
            else:
                return Apartamentos.objects.get(
                    interior__isnull=True,
                    torre=torre,
                    numero=numero
                )
        except Apartamentos.DoesNotExist:
            return None

    def buscar_destinatarios(self, destinatarios_str, emisor=None):
        """
        Busca usuarios por apartamento, correo o grupos especiales.
        
        Formatos de destinatario aceptados:
            - Apartamento con interior: '2-1-301' (interior-torre-numero)
            - Apartamento sin interior: '1-301' (torre-numero)
            - Correo electrónico: 'usuario@email.com'
            - Grupos especiales:
                - 'todos': Todos los usuarios (solo admin)
                - 'propietarios': Todos los propietarios (solo admin)
                - 'administradores', 'administracion': Todos los admins
        
        Acepta múltiples destinatarios separados por coma.
        """
        destinatarios = [d.strip() for d in destinatarios_str.split(',') if d.strip()]
        usuarios_encontrados = []
        no_encontrados = []
        
        es_admin = emisor and emisor.rol == Usuario.Rol_Administrador

        for dest in destinatarios:
            if '@' in dest:
                try:
                    usuario = Usuario.objects.get(correo=dest)
                    usuarios_encontrados.append(usuario)
                    continue
                except Usuario.DoesNotExist:
                    no_encontrados.append(f"{dest} (correo no encontrado)")
                    continue
            
            dest_lower = dest.lower()
            
            if dest_lower == 'todos':
                if es_admin:
                    todos = Usuario.objects.exclude(id_usuario=emisor.id_usuario)
                    usuarios_encontrados.extend(list(todos))
                else:
                    no_encontrados.append(f"{dest} (solo administradores)")
                continue
            
            if dest_lower == 'propietarios':
                if es_admin:
                    propietarios = Usuario.objects.filter(
                        rol=Usuario.Rol_Propietario
                    ).exclude(id_usuario=emisor.id_usuario)
                    usuarios_encontrados.extend(list(propietarios))
                else:
                    no_encontrados.append(f"{dest} (solo administradores)")
                continue
            
            if dest_lower in ['administradores', 'administracion', 'administración']:
                admins = Usuario.objects.filter(rol=Usuario.Rol_Administrador)
                if emisor:
                    admins = admins.exclude(id_usuario=emisor.id_usuario)
                usuarios_encontrados.extend(list(admins))
                continue

            apartamento_data = self.parsear_apartamento(dest)
            
            if apartamento_data:
                interior, torre, numero = apartamento_data
                apartamento = self.buscar_apartamento(interior, torre, numero)
                
                if apartamento and apartamento.id_propietario:
                    usuarios_encontrados.append(apartamento.id_propietario)
                    continue
                elif apartamento:
                    no_encontrados.append(f"{dest} (sin propietario)")
                    continue
                else:
                    no_encontrados.append(f"{dest} (apartamento no existe)")
                    continue

            no_encontrados.append(f"{dest} (formato no válido)")

        usuarios_unicos = []
        ids_vistos = set()
        for usuario in usuarios_encontrados:
            if usuario.id_usuario not in ids_vistos:
                usuarios_unicos.append(usuario)
                ids_vistos.add(usuario.id_usuario)

        return usuarios_unicos, no_encontrados

    def enviar_mensaje(self, emisor, destinatarios_str, categoria, asunto, descripcion, conversacion_id=None):
        """
        Envía un mensaje a uno o múltiples destinatarios.
        Si conversacion_id es None, crea una nueva conversación.
        """
        destinatarios, no_encontrados = self.buscar_destinatarios(destinatarios_str, emisor)

        if not destinatarios:
            return "No se encontraron destinatarios válidos"

        if no_encontrados:
            return f"No se encontraron: {', '.join(no_encontrados)}"

        mensaje = Mensaje.objects.create(
            categoria=categoria,
            asunto=asunto,
            descripcion=descripcion,
            fecha_hora=timezone.now(),
            conversacion=conversacion_id if conversacion_id else 0
        )

        if conversacion_id is None:
            mensaje.conversacion = mensaje.id_mensaje
            mensaje.save()

        UsuarioMensaje.objects.create(
            id_usuario=emisor,
            id_mensaje=mensaje,
            papel='emisor',
            destacado=0,
            leido=1,
            fecha_lectura=timezone.now()
        )

        for destinatario in destinatarios:
            if destinatario.id_usuario != emisor.id_usuario:
                UsuarioMensaje.objects.create(
                    id_usuario=destinatario,
                    id_mensaje=mensaje,
                    papel='receptor',
                    destacado=0,
                    leido=0,
                    fecha_lectura=None
                )

        return None

    def buscar_mensajes(self, usuario, termino, bandeja='recibidos'):
        """Busca mensajes por término en asunto o descripción"""
        if bandeja == 'recibidos':
            mensajes = self.obtener_mensajes_recibidos(usuario)
        elif bandeja == 'enviados':
            mensajes = self.obtener_mensajes_enviados(usuario)
        else:
            mensajes = self.obtener_mensajes_destacados(usuario)

        if termino:
            mensajes = mensajes.filter(
                Q(id_mensaje__asunto__icontains=termino) |
                Q(id_mensaje__descripcion__icontains=termino)
            )

        return mensajes

    def contar_no_leidos(self, usuario):
        """Cuenta los mensajes no leídos del usuario"""
        return UsuarioMensaje.objects.filter(
            id_usuario=usuario,
            papel='receptor',
            leido=0
        ).count()