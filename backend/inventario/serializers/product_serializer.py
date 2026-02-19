from rest_framework import serializers
from inventario.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "presentation", "supplier", "company", "category", "created_at", "updated_at"]
        read_only_fields = ["id", "company", "created_at", "updated_at"]
    
    def create(self, validated_data):
        """
        Create product, company is set from request context
        """
        # Get company from context (set in view)
        company = self.context.get('company')
        if company:
            validated_data['company'] = company
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Update product, preserve company
        """
        validated_data['company'] = instance.company
        return super().update(instance, validated_data)