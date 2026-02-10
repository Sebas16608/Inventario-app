# inventario/views/stock_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from inventario.models.product import Product
from inventario.services.stock_service import StockService
from inventario.serializers.movement_serializer import MovementSerializer

class StockInView(APIView):
    def post(self, request, product_id):
        quantity = request.data.get("quantity")

        if not quantity:
            return Response(
                {"detail": "quantity es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
            movement = StockService.add_stock(
                product=product,
                quantity=int(quantity)
            )
            serializer = MovementSerializer(movement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response(
                {"detail": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class StockOutView(APIView):
    def post(self, request, product_id):
        quantity = request.data.get("quantity")

        if not quantity:
            return Response(
                {"detail": "quantity es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
            movement = StockService.remove_stock(
                product=product,
                quantity=int(quantity)
            )
            serializer = MovementSerializer(movement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response(
                {"detail": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
