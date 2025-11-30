"""Clase de servicios de recuperacion de contraseña"""
from secrets import choice
from random import shuffle
from string import ascii_uppercase,digits
from ..models import Usuario

class RecoveryService:
    """"""
    def configurate_authentication_code(self):
        pass

    def create_authentication_code(self, lenght:int =6, letter_proportion:int =4):
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