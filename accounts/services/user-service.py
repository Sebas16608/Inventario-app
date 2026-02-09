from django.contrib.auth.models import User
from accounts.models import Profile, Company
from django.db import transaction

class UserService:

    @staticmethod
    @transaction.atomic
    def crear_usuario(username, email, password, nombre_empresa=None, rol="SELLER"):
        """
        Crea un usuario, su perfil y su empresa si no existe.
        """
        
        user = User.objects.create_user(username=username, email=email, password=password)

        if not nombre_empresa:
            nombre_empresa = f"Empresa de {username}"
        empresa, _ = Company.objects.get_or_create(nombre=nombre_empresa)

        Profile.objects.create(
            user=user,
            company=empresa,
            role=rol
        )

        return user
