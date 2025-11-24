from django.contrib.auth.hashers import make_password, check_password

class PasswordService:
    
    def hash_password(self, password: str) -> str:
        return make_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return check_password(plain_password, hashed_password)
