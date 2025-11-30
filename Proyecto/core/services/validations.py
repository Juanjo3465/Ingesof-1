"""Validaciones"""
import re
from datetime import date

def validar_nombre(nombre: str):
    """Valida que el nombre sea válido y no contenga números."""
    
    nombre = nombre.strip()

    if not nombre:
        return "El nombre debe existir"

    if len(nombre) < 2:
        return "El nombre debe tener al menos 2 caracteres"

    if len(nombre) > 100:
        return "El nombre no puede tener más de 100 caracteres"

    if re.search(r'\d', nombre):
        return "El nombre no puede contener números"

    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
        return "El nombre solo puede contener letras y espacios"
    
    return ""


def validar_fecha_nacimiento(fecha_nacimiento):
    """ Valida que la fecha de nacimiento sea válida y que la edad esté entre 14 y 150 años """

    if not fecha_nacimiento:
        return "La fecha de nacimiento es obligatoria"
    
    if isinstance(fecha_nacimiento, str):
        try:
            fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
        except ValueError:
            try:
                from datetime import datetime
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%d/%m/%Y').date()
            except ValueError:
                return "Formato de fecha inválido. Use YYYY-MM-DD o DD/MM/YYYY"
    
    hoy = date.today()
    if fecha_nacimiento > hoy:
        return "La fecha de nacimiento no puede ser futura"
    
    edad = hoy.year - fecha_nacimiento.year

    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    if edad < 14:
        return "Debe tener al menos 14 años"

    if edad > 150:
        return "La edad no puede ser mayor a 150 años"
    
    return ""


def validar_correo(correo: str):
    """ Valida que el correo electrónico tenga un formato válido """
    
    correo = correo.strip()

    if not correo:
        return "El correo electrónico es obligatorio"
    

    if len(correo) > 254:  
        return "El correo electrónico es demasiado largo"
    
    # Patrón regex para validar formato de email
    patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(patron_email, correo):
        return "El formato del correo electrónico no es válido"
    
    if ' ' in correo:
        return "El correo electrónico no puede contener espacios"
    
    if correo.count('@') != 1:
        return "El correo electrónico debe contener exactamente un símbolo @"
    
    partes = correo.split('@')
    if not partes[0] or not partes[1]:
        return "El formato del correo electrónico no es válido"
    
    if '.' not in partes[1]:
        return "El dominio del correo debe contener al menos un caracter"
    
    return ""


def validar_celular(celular: str):
    """ Valida que el número de celular tenga exactamente 10 dígitos numéricos """

    celular = celular.strip()

    if not celular:
        return ""
    
    celular_limpio = celular.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

    if not celular_limpio.isdigit():
        return "El celular solo puede contener números"

    if len(celular_limpio) != 10:
        return "El celular debe tener exactamente 10 dígitos"
    
    return ""

def valide_password( password):
    """ Valida que la contraseña cumpla con todos los requisitos de seguridad """
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return "La contraseña debe contener al menos una mayúscula"
    
    if not re.search(r'[a-z]', password):
        return "La contraseña debe contener al menos una minúscula"
    
    if not re.search(r'[0-9]', password):
        return "La contraseña debe contener al menos un número"
    
    if not re.search(r'[@$!%*?&#]', password):
        return "La contraseña debe contener al menos un carácter especial (@$!%*?&#)"
    
    if re.search(r'\s', password):
        return "La contraseña no puede contener espacios"
    
    return ""