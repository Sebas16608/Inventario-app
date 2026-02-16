# inventario/views/stock_view.py
"""
Stock operation API Views with multi-tenant security.
Legacy endpoints for stock in/out operations.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from inventario.models.product import Product
from inventario.services.stock_service import StockService
from inventario.serializers.movement_serializer import MovementSerializer
from inventario.views.base_views import BaseCompanyAPIView


class StockInView(BaseCompanyAPIView):
    """
    Register stock entry for a product.
    Product must belong to user's company.
    
    Endpoint:
    POST /products/{product_id}/stock/in/
    
    Request Body:
        - quantity: int (required)
        - purchase_price: decimal (required)
        - supplier: str (required)
        - expiration_date: date (optional)
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        """
        Register stock entry using StockService.
        
        Args:
            product_id: Product ID to add stock to
            
        Returns:
            Response: Created movement data
        """
        try:
            company = self.get_company()
            quantity = request.data.get("quantity")
            purchase_price = request.data.get("purchase_price")
            supplier = request.data.get("supplier")
            expiration_date = request.data.get("expiration_date")

            # Validate required fields
            if not quantity:
                return Response(
                    {"detail": "quantity is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not purchase_price:
                return Response(
                    {"detail": "purchase_price is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not supplier:
                return Response(
                    {"detail": "supplier is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify product belongs to user's company
            try:
                product = Product.objects.get(id=product_id, company=company)
            except Product.DoesNotExist:
                return Response(
                    {
                        "detail": "Product not found or doesn't belong to your company"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Use StockService to create batch and movement
            batch = StockService.registrar_entrada(
                product=product,
                quantity=int(quantity),
                purchase_price=purchase_price,
                expiration_date=expiration_date,
                supplier=supplier
            )
            
            # Return the created movement
            movement = batch.movements.first()
            serializer = MovementSerializer(movement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exc:
            return Response(
                {"detail": "An error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StockOutView(BaseCompanyAPIView):
    """
    Register stock exit for a product.
    Product must belong to user's company.
    
    Endpoint:
    POST /products/{product_id}/stock/out/
    
    Request Body:
        - quantity: int (required)
        - note: str (optional)
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        """
        Register stock exit using StockService.
        
        Args:
            product_id: Product ID to remove stock from
            
        Returns:
            Response: Created movement data
        """
        try:
            company = self.get_company()
            quantity = request.data.get("quantity")
            note = request.data.get("note")

            # Validate required fields
            if not quantity:
                return Response(
                    {"detail": "quantity is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify product belongs to user's company
            try:
                product = Product.objects.get(id=product_id, company=company)
            except Product.DoesNotExist:
                return Response(
                    {
                        "detail": "Product not found or doesn't belong to your company"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Use StockService to remove stock
            StockService.registrar_salida(
                product=product,
                quantity=int(quantity),
                note=note
            )
            
            # Return the last created movement
            movement = product.batches.latest('id').movements.latest('created_at')
            serializer = MovementSerializer(movement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exc:
            return Response(
                {"detail": "An error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

