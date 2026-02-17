from API import SuperApiView
from accounts.serializers.user_serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class UserView(SuperApiView):
    model = User
    serializer_class = UserSerializer
    filter_fields = ["id", "username", "email"]
    permission_classes = (IsAuthenticated,)