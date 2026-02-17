from rest_framework import serializers

class BatchCreateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = serializers.DateField(required=False)
    supplier = serializers.CharField(max_length=255)
