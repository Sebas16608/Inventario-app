from rest_framework import serializers
from inventario.models.movement import Movement

class MovementSerializer(serializers.ModelSerializer):
    # Nested serializers for related objects
    product = serializers.SerializerMethodField()
    batch_id = serializers.IntegerField(source='batch.id', read_only=True)
    reason = serializers.CharField(source='note', allow_blank=True)
    
    class Meta:
        model = Movement
        fields = [
            "id",
            "batch",
            "batch_id",
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
    batch = serializers.IntegerField()
    product = serializers.IntegerField(required=False)  # For reference only
    movement_type = serializers.ChoiceField(choices=['IN', 'OUT', 'ADJUST', 'EXPIRED'])
    quantity = serializers.IntegerField(min_value=1)
    reason = serializers.CharField(required=False, allow_blank=True)  # Alias for note
