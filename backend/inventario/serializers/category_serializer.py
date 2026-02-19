from rest_framework import serializers
from inventario.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "company", "created_at", "updated_at"]
        read_only_fields = ["id", "company", "created_at", "updated_at"]
    
    def create(self, validated_data):
        """
        Create category, company is set from request context
        """
        # Get company from context (set in view)
        company = self.context.get('company')
        if company:
            validated_data['company'] = company
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Update category, preserve company
        """
        validated_data['company'] = instance.company
        return super().update(instance, validated_data)
