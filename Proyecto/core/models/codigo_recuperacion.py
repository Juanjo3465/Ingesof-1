""" Modelo de codigo de recuperacion """
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import timedelta
from secrets import choice
from random import shuffle
from string import ascii_uppercase,digits


class CodigoRecuperacion(models.Model):
    """"""
    Duration = 10
    Tries=3
    
    username = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255)
    token = models.CharField(max_length=64, unique=True, db_index=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    intentos = models.IntegerField(default=0)
    usado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Código de Recuperación'
        verbose_name_plural = 'Códigos de Recuperación'
        indexes = [
            models.Index(fields=['token', 'usado']),
            models.Index(fields=['username', 'usado']),
        ]

    def is_current(self):
        """
        Verifica si el código está vigente:
        - No ha sido usado
        - No se han agotado los intentos
        - No ha expirado
        """
        if self.usado:
            return False
        
        if self.intentos >= 2:
            return False
        
        if timedelta(minutes= self.Duration) < timezone.now() - self.fecha_creacion:
            return False
        
        return True
    
    @classmethod
    def generate_token(cls):
        """Genera un token único de 64 caracteres"""
        Lenght_token = 64
        chars = [choice(ascii_uppercase + digits) for _ in range(Lenght_token)]
        return ''.join(chars)
    
    @classmethod
    def create_authetication_code(cls,lenght:int =6, letter_proportion:int =4):
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
    
    def send_email(self,codigo):
        """Envía el código de verificación por email"""

        mensaje_texto = f"""
        Hola {self.username},

        Recibimos una solicitud para recuperar tu contraseña.

        Tu código de verificación es: {codigo}

        Este código expira en 10 minutos.

        Si no solicitaste este código, puedes ignorar este mensaje.

        Saludos,
        El equipo de Tu App
                """
                
        try:
            email = EmailMultiAlternatives(
                subject='Código de recuperación de contraseña',
                body=mensaje_texto,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[self.username]
            )
            email.send(fail_silently=False)
            return True
        except Exception as e:
            return False
        
    @classmethod
    def create_object_code(cls, username, codigo):
        token=cls.generate_token()
        codigo_obj=cls.objects.create(
            username=username,
            token=token,
            codigo=make_password(codigo),
        )
        return codigo_obj
        
        
    
    @classmethod
    def send_authentication_code(cls, username):
        """
        Crea un nuevo código de recuperación y lo envía por email.
        Retorna el token si tiene éxito, None si falla.
        """

        cls.objects.filter(username=username, usado=False).delete()
        
        codigo = cls.create_authetication_code()
        
        codigo_obj = cls.create_object_code(username, codigo)

        sended = codigo_obj.send_email(codigo)
        
        if sended:
            return codigo_obj.token
        else:
            codigo_obj.delete()
            return None
    
    @classmethod
    def validate_authentication_code(cls, token, given_code):
        try:
            hash_code_obj = cls.objects.get(token=token, usado=False)
        except cls.DoesNotExist:
            return False
        
        if not hash_code_obj.is_current():
            return False
        
        valide = check_password(given_code, hash_code_obj.codigo)
        
        if valide:
            hash_code_obj.usado = True
            return True
        else:
            hash_code_obj.intentos += 1
            hash_code_obj.save()
            return False
