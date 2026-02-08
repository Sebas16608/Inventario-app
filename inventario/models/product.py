from django.db import models
from inventario.models.category import Category

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    presentation = models.CharField(max_length=255, blank=True, null=True)
    distribuidor = models.CharField(max_length=255)
    # empresa = models.ForeingKey(Empresa, on_delete=models.CASCADE) aqui tambien tengo commiteado empresa por la misma razon de category

    class Meta:
        ordering = ["id"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"Producto {self.name} de {self.category.name}"