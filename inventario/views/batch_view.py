"""
Batch API Views with multi-tenant security.
"""

from rest_framework.response import Response
from rest_framework import status

from inventario.models.batch import Batch
from inventario.models.product import Product
from inventario.serializers.batch_serializer import BatchCreateSerializer
from inventario.views.base_views import BaseCompanyAPIView
from inventario.services.stock_service import StockService


class BatchSerializer:
    """Simple serializer for Batch responses."""
    
    @staticmethod
    def serialize(batch):
        return {
            "id": batch.id,
            "product_id": batch.product.id,
            "quantity_received": batch.quantity_received,
            "quantity_available": batch.quantity_available,
            "purchase_price": str(batch.purchase_price),
            "expiration_date": batch.expiration_date,
            "received_at": batch.received_at,
            "supplier": batch.supplier,
        }


class BatchAPIView(BaseCompanyAPIView):
    """
    Secure Batch API View with multi-tenant isolation.
    
    Features:
    - Only lists/modifies batches for products in user's company
    - Product must belong to user's company
    - Uses StockService for safe batch creation
    
    Endpoints:
    - GET /batches/ → List batches for user's company products
    - POST /batches/ → Create batch for user's company product
    - GET /batches/{id}/ → Retrieve only if product belongs to user's company
    - DELETE /batches/{id}/ → Delete only if product belongs to user's company
    """
    
    model = Batch
    serializer_class = BatchCreateSerializer

    def get(self, request, pk=None):
        """
        List batches or retrieve a specific batch.
        Only shows batches for products in user's company.
        
        Query Parameters:
            - product_id: Filter by product ID (optional)
            
        Args:
            pk: Optional batch ID
            
        Returns:
            Response: Batch data or list
        """
        try:
            company = self.get_company()
            
            # Base queryset: only batches of products in user's company
            base_queryset = Batch.objects.filter(product__company=company)
            
            if pk is not None:
                # Retrieve specific batch
                batch = base_queryset.get(pk=pk)
                return Response(
                    BatchSerializer.serialize(batch),
                    status=status.HTTP_200_OK
                )

            # List with optional product filter
            product_id = request.query_params.get('product_id')
            if product_id:
                queryset = base_queryset.filter(product_id=product_id)
            else:
                queryset = base_queryset

            if not queryset.exists():
                return Response([], status=status.HTTP_200_OK)

            data = [BatchSerializer.serialize(batch) for batch in queryset]
            return Response(data, status=status.HTTP_200_OK)

        except Exception as exc:
            return self.handle_exception(exc)

    def post(self, request):
        """
        Create a new batch for a product in user's company.
        Uses StockService to ensure data consistency.
        
        Required Fields:
            - product_id: int
            - quantity: int (quantity_received)
            - purchase_price: decimal
            - supplier: str
            
        Optional Fields:
            - expiration_date: date
            
        Returns:
            Response: Created batch data
        """
        try:
            company = self.get_company()
            
            # Validate serializer structure
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get product and validate it belongs to user's company
            product_id = request.data.get('product_id')
            if not product_id:
                return Response(
                    {"detail": "product_id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                product = Product.objects.get(
                    id=product_id,
                    company=company
                )
            except Product.DoesNotExist:
                return Response(
                    {
                        "detail": "Product not found or doesn't belong to your company"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Use StockService to create batch (ensures data consistency)
            batch = StockService.registrar_entrada(
                product=product,
                quantity=serializer.validated_data['quantity'],
                purchase_price=serializer.validated_data['purchase_price'],
                expiration_date=serializer.validated_data.get('expiration_date'),
                supplier=serializer.validated_data['supplier']
            )
            
            return Response(
                BatchSerializer.serialize(batch),
                status=status.HTTP_201_CREATED
            )

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exc:
            return self.handle_exception(exc)

    def delete(self, request, pk):
        """
        Delete batch (product must belong to user's company).
        
        Args:
            pk: Batch ID
            
        Returns:
            Response: Empty response with 204 status
        """
        try:
            company = self.get_company()
            
            batch = Batch.objects.filter(product__company=company).get(pk=pk)
            batch.delete()
            
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Batch.DoesNotExist:
            return Response(
                {"detail": "Batch not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as exc:
            return self.handle_exception(exc)
