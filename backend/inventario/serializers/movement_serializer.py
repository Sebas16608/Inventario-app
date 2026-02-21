from rest_framework import serializers
from inventario.models.movement import Movement

class MovementSerializer(serializers.ModelSerializer):
    # Nested serializers for related objects
    product = serializers.SerializerMethodField()
    batch_id = serializers.IntegerField(source='batch.id', read_only=True)
    batch_code = serializers.CharField(source='batch.code', read_only=True)
    reason = serializers.CharField(source='note', allow_blank=True)
    
    class Meta:
        model = Movement
        fields = [
            "id",
            "batch",
            "batch_id",
            "batch_code",
            "product",
            "movement_type",
            "quantity",
            "reason",
            "created_at",
        ]
    
    def get_product(self, obj):
        """Return product ID from the batch."""
        return obj.batch.product.id

class MovementCreateSerializer(serializers.Serializer):
    """Serializer for creating movements with POST requests."""
    batch_code = serializers.CharField(required=False)
    batch = serializers.IntegerField(required=False)
    product = serializers.IntegerField(required=False)
    movement_type = serializers.ChoiceField(choices=['IN', 'OUT', 'ADJUST', 'EXPIRED'])
    quantity = serializers.IntegerField(min_value=1)
    reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        if not data.get('batch_code') and not data.get('batch'):
            raise serializers.ValidationError("Se requiere batch_code o batch")
        return data
