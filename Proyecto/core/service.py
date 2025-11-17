import re
import datetime


# ============================================================
# VALIDACIÓN DE CONTRASEÑA SIMPLE
# ============================================================

def solicitar_contrasena_simple():
    """
    Solicita dos contraseñas y valida que coincidan.
    Vuelve a pedir si no son iguales.
    """
    while True:
        nueva = input("Ingrese nueva contraseña: ")
        confirmar = input("Confirme nueva contraseña: ")

        if nueva == confirmar:
            print("\n✅ Contraseña válida.")
            return nueva
        else:
            print("\n❌ Las contraseñas no coinciden. Inténtelo nuevamente.\n")


# ============================================================
# VALIDACIÓN DE FECHA
# ============================================================

def solicitar_fecha_valida():
    """
    Solicita una fecha en formato día-mes-año o día/mes/año
    y valida que sea una fecha real y un año entre 1950 y 2099.
    """
    patron = r"^\d{1,2}[-/]\d{1,2}[-/]\d{4}$"

    while True:
        fecha_str = input("Ingrese fecha (día-mes-año): ")

        if not re.match(patron, fecha_str):
            print("❌ Formato inválido. Use 12-03-2024 o 12/03/2024.\n")
            continue

        separador = "-" if "-" in fecha_str else "/"
        dia, mes, anio = map(int, fecha_str.split(separador))

        if not (1950 <= anio <= 2099):
            print("❌ Año fuera del rango permitido (1950 a 2099).\n")
            continue

        try:
            fecha_valida = datetime.date(anio, mes, dia)
            print("✅ Fecha válida:", fecha_valida.strftime("%d-%m-%Y"))
            return fecha_valida
        except ValueError:
            print("❌ La fecha no existe.\n")


# ============================================================
# VALIDACIÓN DE ASUNTO Y DESCRIPCIÓN
# ============================================================

def validar_asunto(asunto):
    """
    Valida el asunto:
    - Solo caracteres permitidos (texto simple)
    - Longitud entre 5 y 60 caracteres
    """
    patron = r"^[A-Za-z0-9 áéíóúÁÉÍÓÚñÑ.,;:!?()-]+$"
    if not re.match(patron, asunto):
        return "El asunto contiene caracteres no permitidos."
    if not (5 <= len(asunto) <= 60):
        return "El asunto debe tener entre 5 y 60 caracteres."
    return None


def validar_descripcion(descripcion):
    """
    Valida la descripción:
    - Mínimo 10 caracteres
    - Máximo 500 caracteres
    """
    if len(descripcion) < 10:
        return "La descripción debe tener al menos 10 caracteres."
    if len(descripcion) > 500:
        return "La descripción no puede exceder los 500 caracteres."
    return None


def solicitar_peticion():
    """
    Pide al usuario un asunto y descripción hasta que ambos sean válidos.
    """
    while True:
        asunto = input("Ingrese el asunto: ")
        error_asunto = validar_asunto(asunto)

        if error_asunto:
            print(f"❌ {error_asunto}\n")
            continue

        descripcion = input("Ingrese la descripción: ")
        error_desc = validar_descripcion(descripcion)

        if error_desc:
            print(f"❌ {error_desc}\n")
            continue

        print("\n✅ Petición válida.")
        return asunto, descripcion


# ============================================================
# EJEMPLO DE USO
# ============================================================

