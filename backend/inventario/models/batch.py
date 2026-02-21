from django.db import models
from inventario.models.product import Product


class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="batches")
    quantity_received = models.IntegerField()
    quantity_available = models.IntegerField()
    purchase_price = models.DecimalField(decimal_places=2, max_digits=10)
    expiration_date = models.DateField()
    received_at = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Batch"
        verbose_name_plural = "Batches"

    def __str__(self):
        return f"De {self.product.name} hay {self.quantity_available} y se recibieron {self.quantity_received}"