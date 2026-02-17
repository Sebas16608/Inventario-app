from API import SuperApiView
from accounts.serializers.profile_serializer import ProfileSerializer
from accounts.models import Profile
from rest_framework.permissions import IsAuthenticated

class ProfileView(SuperApiView):
    model = Profile
    serializer_class = ProfileSerializer
    filter_fields = ["id", "user", "company", "role"]
    permission_classes = (IsAuthenticated,)