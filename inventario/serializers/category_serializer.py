from rest_framework import serializers
from inventario.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "company", "created_at", "updated_at"]
