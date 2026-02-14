from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(username = data["username"], password = data["password"])

        if not user:
            raise serializers.ValidationError("Usuario o contraseñano incorrectos")
        data['user'] = user
        return data