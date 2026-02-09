from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Administrador"),
        ("SELLER", "Vendedor"),
        ("WAREHOUSE", "Almacén"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="profiles")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="SELLER")

    class Meta:
        ordering = ["id"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
    
    def __str__(self):
        return f"Perfil de {self.user.username} de {self.company.name} con el rol {self.role}"