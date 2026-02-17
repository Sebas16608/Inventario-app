"""
Base API views for multi-tenant security.
All views must enforce company isolation.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class BaseCompanyAPIView(APIView):
    """
    Base class for all company-aware API views.
    
    Features:
    - Enforces IsAuthenticated permission
    - Gets company from request.user.profile.company (NEVER from request body)
    - Validates all objects belong to user's company
    
    Subclasses must implement:
    - model: Django model class
    - serializer_class: DRF Serializer class
    """
    
    permission_classes = [IsAuthenticated]
    model = None
    serializer_class = None

    def get_company(self):
        """
        Get company from authenticated user's profile.
        NEVER trust company from request body.
        
        Returns:
            Company: User's associated company
            
        Raises:
            ValueError: If user has no profile or company
            PermissionError: If user is not authenticated
        """
        # Verify user is authenticated
        if not self.request.user.is_authenticated:
            raise PermissionError("User must be authenticated")
        
        try:
            return self.request.user.profile.company
        except AttributeError:
            raise ValueError("User does not have a profile or company assigned")

    def get_company_queryset(self):
        """
        Get filtered queryset for user's company.
        
        Returns:
            QuerySet: Objects filtered by company
        """
        company = self.get_company()
        return self.model.objects.filter(company=company)

    def validate_company_ownership(self, obj):
        """
        Validate that object belongs to user's company.
        
        Args:
            obj: Object to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            PermissionError: If object doesn't belong to user's company
        """
        company = self.get_company()
        
        if hasattr(obj, 'company') and obj.company != company:
            raise PermissionError(
                "You don't have permission to access this resource"
            )
        
        return True

    def handle_exception(self, exc):
        """
        Handle exceptions with proper DRF responses.
        
        Args:
            exc: Exception to handle
            
        Returns:
            Response: DRF Response with appropriate status code
        """
        if isinstance(exc, PermissionError):
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_403_FORBIDDEN
            )
        elif isinstance(exc, ValueError):
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, self.model.DoesNotExist):
            return Response(
                {"detail": "Resource not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            {"detail": "An error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
