"""
Product API Views with multi-tenant security.
"""

from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

from inventario.models.product import Product
from inventario.models.category import Category
from inventario.serializers.product_serializer import ProductSerializer
from inventario.views.base_views import BaseCompanyAPIView


class ProductAPIView(BaseCompanyAPIView):
    """
    Secure Product API View with multi-tenant isolation.
    
    Features:
    - Only lists/modifies products belonging to user's company
    - Category must belong to same company as product
    - Company is automatically assigned on creation
    
    Endpoints:
    - GET /products/ → List user's company products
    - POST /products/ → Create product in user's company
    - GET /products/{id}/ → Retrieve only if belongs to user's company
    - PUT /products/{id}/ → Update only if belongs to user's company
    - PATCH /products/{id}/ → Partial update only if belongs to user's company
    - DELETE /products/{id}/ → Delete only if belongs to user's company
    """
    
    model = Product
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        """
        List products or retrieve a specific product.
        
        Query Parameters:
            - name: Filter by name
            - slug: Filter by slug
            - supplier: Filter by supplier
            
        Args:
            pk: Optional product ID
            
        Returns:
            Response: Product data or list
        """
        try:
            if pk is not None:
                # Retrieve specific product
                product = self.get_company_queryset().get(pk=pk)
                serializer = self.serializer_class(product)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # List with optional filters
            filters = {}
            for field in ['name', 'slug', 'supplier']:
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
        Create a new product for user's company.
        Company is automatically assigned (NOT from request body).
        Category must belong to same company.
        
        Required Fields:
            - name: str
            - slug: str (unique per company)
            - category: int (category ID)
            - supplier: str
            
        Optional Fields:
            - presentation: str
            
        Returns:
            Response: Created product data
        """
        try:
            company = self.get_company()
            
            # Validate that category belongs to same company
            category_id = request.data.get('category')
            if category_id:
                try:
                    category = Category.objects.get(
                        id=category_id,
                        company=company
                    )
                except Category.DoesNotExist:
                    return Response(
                        {
                            "detail": "Category not found or doesn't belong to your company"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
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
            logger.error(f"Error inesperado en POST /products/: {str(e)}")
            traceback.print_exc()
            return Response(
                {"error": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        """
        Update entire product (must belong to user's company).
        Company cannot be changed.
        
        Args:
            pk: Product ID
            
        Returns:
            Response: Updated product data
        """
        try:
            company = self.get_company()
            product = self.get_company_queryset().get(pk=pk)
            self.validate_company_ownership(product)
            
            # Validate category if provided
            category_id = request.data.get('category')
            if category_id and category_id != product.category.id:
                try:
                    Category.objects.get(id=category_id, company=company)
                except Category.DoesNotExist:
                    return Response(
                        {
                            "detail": "Category not found or doesn't belong to your company"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Pass company in context
            serializer = self.serializer_class(
                product,
                data=request.data,
                context={'company': product.company}
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
        Partial update product (must belong to user's company).
        Company cannot be changed.
        
        Args:
            pk: Product ID
            
        Returns:
            Response: Updated product data
        """
        try:
            company = self.get_company()
            product = self.get_company_queryset().get(pk=pk)
            self.validate_company_ownership(product)
            
            # Validate category if provided
            category_id = request.data.get('category')
            if category_id and category_id != product.category.id:
                try:
                    Category.objects.get(id=category_id, company=company)
                except Category.DoesNotExist:
                    return Response(
                        {
                            "detail": "Category not found or doesn't belong to your company"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Pass company in context and use partial=True
            serializer = self.serializer_class(
                product,
                data=request.data,
                partial=True,
                context={'company': product.company}
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
        Delete product (must belong to user's company).
        
        Args:
            pk: Product ID
            
        Returns:
            Response: Empty response with 204 status
        """
        try:
            product = self.get_company_queryset().get(pk=pk)
            self.validate_company_ownership(product)
            
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exc:
            return self.handle_exception(exc)
