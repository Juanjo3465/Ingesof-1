from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from .account_service import AccountService

class PasswordService:
    
    def hash_password(self, password: str) -> str:
        return make_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return check_password(plain_password, hashed_password)
    
    def change_password(self, user:User, new_password:str):
        account = AccountService()
        usuario = account.get_app_user(user)
        
        usuario.contrasena = self.hash_password(new_password)
        usuario.save()
