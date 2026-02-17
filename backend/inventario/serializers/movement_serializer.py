from rest_framework import serializers
from inventario.models.movement import Movement

class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = [
            "id",
            "movement_type",
            "quantity",
            "created_at",
        ]
