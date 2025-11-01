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
    # Esta parte se ejecuta si el usuario está ENVIANDO el formulario (método POST)
    if request.method == 'POST':
        # 1. Recogemos los datos del formulario.
        #    request.POST.get() busca el dato por el atributo 'name' del input/select en el HTML.
        zona_comun_id = request.POST.get('zona_comun')
        fecha_reserva_str = request.POST.get('fecha_reserva')
        hora_reserva_str = request.POST.get('hora_reserva')
        
        # (Simplificación) Por ahora, asignaremos la reserva a un usuario existente.
        # Más adelante, esto se hará con el usuario que ha iniciado sesión.
        # Asegúrate de tener un usuario con id=1 o cambia el número.
        try:
            usuario_actual = Usuario.objects.get(pk=1)
        except Usuario.DoesNotExist:
            # Manejar el caso en que el usuario no exista, quizás redirigir con un error.
            # Por ahora, para la prueba, asumimos que existe.
            return redirect('crear_reserva') # Vuelve al formulario si el usuario no existe

        # 2. Obtenemos el objeto completo de la ZonaComun a partir de su ID.
        zona_comun_obj = ZonaComun.objects.get(pk=zona_comun_id)

        # 3. Combinamos la fecha y la hora.
        #    (Esta es una forma simple, se puede hacer más robusta)
        fecha_hora_completa = f"{fecha_reserva_str} {hora_reserva_str}"

        # 4. Creamos el nuevo registro de Reserva en la base de datos.
        Reserva.objects.create(
            id_zona_comun=zona_comun_obj,
            id_usuario=usuario_actual,
            fecha_hora=fecha_hora_completa,
            # Valores de ejemplo para los campos restantes, puedes ajustarlos.
            cantidad_personas=10,
            duracion=2, # en horas
            costo=0.00,
            estado='Confirmada'
        )

        # 5. Redirigimos al usuario a la lista de reservas para que vea su nueva reserva.
        #    'lista_de_reservas' es el 'name' que le dimos a la URL en reservas/urls.py.
        return redirect('lista_de_reservas')

    # Esta parte se ejecuta si el usuario solo está VISITANDO la página (método GET)
    else:
        zonas_disponibles = ZonaComun.objects.all()
        contexto = {
            'zonas': zonas_disponibles
        }
        return render(request, 'reservas/crear_reservas.html', contexto)