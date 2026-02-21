from rest_framework import serializers
from inventario.models.batch import Batch
from inventario.models.product import Product

class BatchSerializer(serializers.ModelSerializer):
    """Serializer for Batch responses."""
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = Batch
        fields = [
            "id",
            "code",
            "product",
            "quantity_received",
            "quantity_available",
            "purchase_price",
            "expiration_date",
            "supplier",
            "received_at",
        ]
        read_only_fields = [
            "id",
            "code",
            "received_at",
        ]

class BatchCreateSerializer(serializers.Serializer):
    """Serializer for creating batches with POST requests."""
    product = serializers.IntegerField()
    quantity_received = serializers.IntegerField(min_value=1)
    quantity_available = serializers.IntegerField(required=False)
    purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = serializers.DateField(required=True)
    supplier = serializers.CharField(max_length=255)
