from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import Company
from accounts.serializers.company_serializer import CompanySerializer
from inventario.views.base_views import BaseCompanyAPIView


class CompanyView(BaseCompanyAPIView):
    """
    Secure Company API View - users can only access their own company.
    
    Features:
    - Users can only view their own company
    - No listing of all companies (security: don't leak competitor data)
    
    Endpoints:
    - GET /companies/ → Returns your own company
    - GET /companies/{id}/ → Returns your own company if ID matches
    """
    
    model = Company
    serializer_class = CompanySerializer

    def get(self, request, pk=None):
        try:
            user_company = self.get_company()
            
            if pk is not None:
                if int(pk) != user_company.id:
                    return Response(
                        {"detail": "You can only access your own company"},
                        status=status.HTTP_403_FORBIDDEN
                    )
                company = user_company
            else:
                company = user_company

            serializer = self.serializer_class(company)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return Response(
                {"detail": "Company not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as exc:
            return self.handle_exception(exc)
