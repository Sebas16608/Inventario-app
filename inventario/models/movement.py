from django.db import models
from inventario.models.batch import Batch

class Movement(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="movements")
    TYPES = [
        ("IN", "Entrada"),
        ("OUT", "Salida"),
        ("ADJUST", "Ajuste"),
        ("EXPIRED", "Expirado")
    ]
    movement_type = models.CharField(max_length=7, choices=TYPES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Movement"
        verbose_name_plural = "Movements"

    def __str__(self):
        return self.movement_type