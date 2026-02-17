from API import SuperApiView
from accounts.models import Company
from accounts.serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated

class CompanyView(SuperApiView):
    model = Company
    serializer_class = CompanySerializer
    filter_fields = ["name", "created_at"]
    permission_classes = (IsAuthenticated,)