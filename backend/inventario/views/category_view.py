"""
Category API Views with multi-tenant security.
"""

from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

from inventario.models.category import Category
from inventario.serializers.category_serializer import CategorySerializer
from inventario.views.base_views import BaseCompanyAPIView


class CategoryAPIView(BaseCompanyAPIView):
    """
    Secure Category API View with multi-tenant isolation.
    
    Endpoints:
    - GET /categories/ → List user's company categories
    - POST /categories/ → Create category in user's company
    - GET /categories/{id}/ → Retrieve only if belongs to user's company
    - PUT /categories/{id}/ → Update only if belongs to user's company
    - PATCH /categories/{id}/ → Partial update only if belongs to user's company
    - DELETE /categories/{id}/ → Delete only if belongs to user's company
    """
    
    model = Category
    serializer_class = CategorySerializer

    def get(self, request, pk=None):
        """
        List categories or retrieve a specific category.
        
        Query Parameters:
            - name: Filter by name
            - slug: Filter by slug
            
        Args:
            pk: Optional category ID
            
        Returns:
            Response: Category data or list
        """
        try:
            if pk is not None:
                # Retrieve specific category
                category = self.get_company_queryset().get(pk=pk)
                serializer = self.serializer_class(category)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # List with optional filters
            filters = {}
            for field in ['name', 'slug']:
                value = request.query_params.get(field)
                if value is not None:
                    filters[field] = value

            queryset = self.get_company_queryset().filter(**filters)

            if not queryset.exists():
                return Response([], status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as exc:
            return self.handle_exception(exc)

    def post(self, request):
        """
        Create a new category for user's company.
        Company is automatically assigned (NOT from request body).
        
        Required Fields:
            - name: str
            - slug: str (unique per company)
            
        Optional Fields:
            - description: str
            
        Returns:
            Response: Created category data
        """
        try:
            # Get company from user profile
            company = self.get_company()
            
            # Pass company in context, not in data
            serializer = self.serializer_class(
                data=request.data,
                context={'company': company}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except (ValueError, AttributeError) as e:
            return Response(
                {"error": f"Error de configuración: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            import traceback
            logger.error(f"Error inesperado en POST /categories/: {str(e)}")
            traceback.print_exc()
            return Response(
                {"error": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        """
        Update entire category (must belong to user's company).
        Company cannot be changed.
        
        Args:
            pk: Category ID
            
        Returns:
            Response: Updated category data
        """
        try:
            category = self.get_company_queryset().get(pk=pk)
            self.validate_company_ownership(category)
            
            # Pass company in context for serializer
            serializer = self.serializer_class(
                category,
                data=request.data,
                context={'company': category.company}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as exc:
            return self.handle_exception(exc)

    def patch(self, request, pk):
        """
        Partial update category (must belong to user's company).
        Company cannot be changed.
        
        Args:
            pk: Category ID
            
        Returns:
            Response: Updated category data
        """
        try:
            category = self.get_company_queryset().get(pk=pk)
            self.validate_company_ownership(category)
            
            # Pass company in context and use partial=True
            serializer = self.serializer_class(
                category,
                data=request.data,
                partial=True,
                context={'company': category.company}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as exc:
            return self.handle_exception(exc)

    def delete(self, request, pk):
        """
        Delete category (must belong to user's company).
        
        Args:
            pk: Category ID
            
        Returns:
            Response: Empty response with 204 status
        """
        try:
            category = self.get_company_queryset().get(pk=pk)
            self.validate_company_ownership(category)
            
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exc:
            return self.handle_exception(exc) 
