from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from accounts.serializers.profile_serializer import ProfileSerializer
from inventario.views.base_views import BaseCompanyAPIView


class ProfileView(BaseCompanyAPIView):
    """
    Secure Profile API View with multi-tenant isolation.
    
    Features:
    - Only lists profiles belonging to user's company
    
    Endpoints:
    - GET /profiles/ → List profiles in your company
    - GET /profiles/{id}/ → Retrieve profile only if in your company
    """
    
    model = Profile
    serializer_class = ProfileSerializer

    def get(self, request, pk=None):
        try:
            company = self.get_company()
            
            if pk is not None:
                profile = Profile.objects.filter(company=company).get(pk=pk)
                serializer = self.serializer_class(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = Profile.objects.filter(company=company)

            if not queryset.exists():
                return Response([], status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile not found or doesn't belong to your company"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as exc:
            return self.handle_exception(exc)
