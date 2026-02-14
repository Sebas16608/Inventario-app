from API import SuperApiView
from accounts.models import Company
from accounts.serializers import CompanySerializer

class CompanyView(SuperApiView):
    model = Company
    serializer_class = CompanySerializer
    filter_fields = ["name", "created_at"]