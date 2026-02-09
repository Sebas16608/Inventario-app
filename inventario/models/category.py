from django.db import models
from accounts.models import Company

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        constraints = [
        models.UniqueConstraint(
            fields=["company", "slug"],
            name="unique_category_slug_per_company"
        )
    ]

    def __str__(self):
        return self.name