from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from accounts.serializers.user_serializer import UserSerializer
from inventario.views.base_views import BaseCompanyAPIView


class UserView(BaseCompanyAPIView):
    """
    Secure User API View with multi-tenant isolation.
    
    Features:
    - Only lists users belonging to user's company
    - User data is linked via Profile to Company
    
    Endpoints:
    - GET /users/ → List users in your company
    - GET /users/{id}/ → Retrieve user only if in your company
    """
    
    model = User
    serializer_class = UserSerializer

    def get(self, request, pk=None):
        try:
            company = self.get_company()
            
            if pk is not None:
                user = User.objects.filter(profile__company=company).get(pk=pk)
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            queryset = User.objects.filter(profile__company=company)

            if not queryset.exists():
                return Response([], status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "User not found or doesn't belong to your company"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as exc:
            return self.handle_exception(exc)
