from django.contrib.auth.models import User
from ..models import Apartamentos, Residente
from .services import AccountService

class ApartmentService:
    def get_resident_apartment(self,user: User):
        account = AccountService()
        usuario = account.get_app_user(user)

        try:
            residencia = Residente.objects.get(id_usuario=usuario.id_usuario)
        except Residente.DoesNotExist:
            return None

        return residencia.id_apartamento
        
    def get_owner_apartments(self,user: User):
        account = AccountService()
        usuario = account.get_app_user(user)

        apartments = Apartamentos.objects.filter(id_propietario=usuario.id_usuario)

        if not apartments.exists():  
            return None

        return apartments
    
    def get_residents(self, apartment: Apartamentos):
        residents = (
            Residente.objects
            .filter(id_apartamento=apartment)
            .select_related("id_usuario")
            .only("id_usuario")
        )

        if not residents.exists():
            return None

        return residents
        
    def get_owner(self, apartment:Apartamentos):
        owner = apartment.id_propietario
        return owner
