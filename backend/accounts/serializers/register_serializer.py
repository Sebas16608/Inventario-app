from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Profile, Company


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "company_id"]

    def create(self, validated_data):
        company_id = validated_data.pop("company_id")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        company = Company.objects.get(id=company_id)

        Profile.objects.create(
            user=user,
            company=company,
            role="SELLER"  # default
        )

        return user
