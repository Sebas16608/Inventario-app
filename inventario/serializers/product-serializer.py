from rest_framework import serializers
from inventario.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "presentation", "distribuidor", "company", "category", "created_at", "updated_at"]