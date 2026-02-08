from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    # empresa = models.ForeingKey(Empresa, on_delete=models.CASCADE, related_name="category") Esto con commit porque aun no tengo nada de cuentas, usuarios ni empresas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    #     constraints = [
    #     models.UniqueConstraint(
    #         fields=["empresa", "slug"],
    #         name="unique_category_slug_per_company"
    #     )
    # ]