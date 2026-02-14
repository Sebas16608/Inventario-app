from API import SuperApiView
from accounts.serializers.user_serializer import UserSerializer
from django.contrib.auth.models import User

class UserView(SuperApiView):
    model = User
    serializer_class = UserSerializer
    filter_fields = ["id", "username", "email"]
