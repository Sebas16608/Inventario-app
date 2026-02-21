from django.db import models
from inventario.models.product import Product


class Batch(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="batches"
    )

    code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    quantity_received = models.IntegerField()

    quantity_available = models.IntegerField()

    purchase_price = models.DecimalField(
        decimal_places=2,
        max_digits=10
    )

    expiration_date = models.DateField(
        blank=True,
        null=True
    )

    received_at = models.DateTimeField(
        auto_now_add=True
    )

    supplier = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ["id"]

        verbose_name = "Batch"
        verbose_name_plural = "Batches"

        constraints = [
            models.UniqueConstraint(
                fields=["product", "code"],
                name="unique_batch_code_per_product"
            )
        ]

    def __str__(self):
        return f"Lote {self.code} - {self.product.name}"