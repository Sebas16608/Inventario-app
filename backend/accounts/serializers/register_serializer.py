from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile, Company


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    company_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "company_id", "company_name"]

    def validate_username(self, value):
        """Validar que el username sea único"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso")
        return value
    
    def validate_email(self, value):
        """Validar que el email sea único"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value

    def validate(self, data):
        """Validar que al menos company_id o company_name esté presente"""
        company_id = data.get("company_id")
        company_name = data.get("company_name")
        
        if not company_id and not company_name:
            raise serializers.ValidationError("Debe proporcionar company_id o company_name")
        
        return data

    def create(self, validated_data):
        company_id = validated_data.pop("company_id", None)
        company_name = validated_data.pop("company_name", "")
        password = validated_data.pop("password")

        # Crear o obtener la empresa
        if company_id:
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                raise serializers.ValidationError("La empresa especificada no existe")
        else:
            # Crear nueva empresa si no existe
            company, created = Company.objects.get_or_create(name=company_name)

        # Crear usuario
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Crear perfil con rol ADMIN para el creador
        Profile.objects.create(
            user=user,
            company=company,
            role="ADMIN"  # El que registra es administrador
        )

        return user
