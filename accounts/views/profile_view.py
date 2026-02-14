from API import SuperApiView
from accounts.serializers.profile_serializer import ProfileSerializer
from accounts.models import Profile

class ProfileView(SuperApiView):
    model = Profile
    serializer_class = ProfileSerializer
    filter_fields = ["id", "user", "company", "role"]