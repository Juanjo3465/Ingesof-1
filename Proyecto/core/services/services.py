"""Funciones servicios"""
from re import match
from secrets import choice
from random import shuffle
from string import ascii_uppercase,digits

def create_autetication_code(lenght:int =6, letter_proportion:int =4):
    """"""
    if lenght < letter_proportion:
        letter_proportion=lenght
    if letter_proportion < 0:
        letter_proportion=0

    chars = (
        [choice(ascii_uppercase) for _ in range(letter_proportion)] +
        [choice(digits) for _ in range(lenght-letter_proportion)]
    )
    shuffle(chars)
    return ''.join(chars)

def valid_code(code:str,lenght:int,letter_proportion:int):
    """"""  
    numeric_proportion=lenght-letter_proportion

    sum_numeric=0
    sum_letter=0

    for c in code:
        if c.isdigit():
            sum_numeric+=1
        elif c.isalpha():
            sum_letter+=1

    if letter_proportion != sum_letter:
        return False

    if numeric_proportion != sum_numeric:
        return False

    return True

def equials_strings(string_1:str,string_2:str):
    """"""
    return string_1 == string_2

def validar_asunto(asunto):
    """
    Valida el asunto:
    - Solo caracteres permitidos (texto simple)
    - Longitud entre 5 y 60 caracteres
    """
    patron = r"^[A-Za-z0-9 áéíóúÁÉÍÓÚñÑ.,;:!?()-]+$"
    if not match(patron, asunto):
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
            print(f" {error_asunto}\n")
            continue

        descripcion = input("Ingrese la descripción: ")
        error_desc = validar_descripcion(descripcion)

        if error_desc:
            print(f" {error_desc}\n")
            continue

        print("\n Petición válida.")
        return asunto, descripcion
