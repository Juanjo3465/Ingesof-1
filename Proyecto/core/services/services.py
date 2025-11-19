"""Funciones servicios"""
from re import match, search
from secrets import choice
from random import shuffle
from string import ascii_uppercase,digits

def is_valid_email(email:str):
    """"""
    # Patron: String @ email . extention
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"
    if match(email_regex,email):
        return True
    return False

def is_valid_password(password:str):
    """"""
    if len(password) < 8:
        return False
    # Si no hay una mayuscula
    if not search(r"[A-Z]",password):
        return False
    # Si no hay una minuscula
    if not search(r"[a-z]",password):
        return False
    # Si no hay un numero
    if not search(r"[0-9]",password):
        return False
    if " " in password:
        return False
    return True

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
