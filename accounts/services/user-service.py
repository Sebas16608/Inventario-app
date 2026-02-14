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

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Crear o buscar empresa
        if not nombre_empresa:
            nombre_empresa = f"Empresa de {username}"

        empresa, _ = Company.objects.get_or_create(name=nombre_empresa)

        # Crear perfil
        Profile.objects.create(
            user=user,
            company=empresa,
            role=rol
        )

        return user
