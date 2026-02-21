"""
Movement API Views with multi-tenant security.
"""

from rest_framework.response import Response
from rest_framework import status

from inventario.models.movement import Movement
from inventario.models.batch import Batch
from inventario.serializers.movement_serializer import MovementSerializer, MovementCreateSerializer
from inventario.views.base_views import BaseCompanyAPIView
from inventario.services.stock_service import StockService


class MovementAPIView(BaseCompanyAPIView):
    """
    Secure Movement API View with multi-tenant isolation.
    
    Features:
    - Only lists/modifies movements for batches in user's company
    - Batch must belong to a product in user's company
    - Uses StockService for safe movement creation
    
    Endpoints:
    - GET /movements/ → List movements for user's company batches
    - POST /movements/ → Create movement (stock in/out/adjust)
    - GET /movements/{id}/ → Retrieve only if batch belongs to user's company
    
    Movement Types:
    - IN: Product stock entry
    - OUT: Product stock exit
    - ADJUST: Manual adjustment
    - EXPIRED: Mark batch as expired
    """
    
    model = Movement
    serializer_class = MovementSerializer

    def get(self, request, pk=None):
        """
        List movements or retrieve a specific movement.
        Only shows movements for batches of products in user's company.
        
        Query Parameters:
            - batch_id: Filter by batch ID (optional)
            - movement_type: Filter by type (IN, OUT, ADJUST, EXPIRED)
            
        Args:
            pk: Optional movement ID
            
        Returns:
            Response: Movement data or list
        """
        try:
            company = self.get_company()
            
            # Base queryset: only movements of batches in user's company
            base_queryset = Movement.objects.filter(batch__product__company=company)
            
            if pk is not None:
                # Retrieve specific movement
                movement = base_queryset.get(pk=pk)
                serializer = self.serializer_class(movement)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # List with optional filters
            filters = {}
            
            batch_id = request.query_params.get('batch_id')
            if batch_id:
                filters['batch_id'] = batch_id
            
            movement_type = request.query_params.get('movement_type')
            if movement_type:
                filters['movement_type'] = movement_type

            queryset = base_queryset.filter(**filters)

            if not queryset.exists():
                return Response([], status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as exc:
            return self.handle_exception(exc)

    def post(self, request):
        """
        Create a new movement (stock in/out/adjust).
        Uses StockService to ensure data consistency.
        
        Required Fields (varies by movement_type):
            - batch: int (batch ID)
            - movement_type: str (IN, OUT, ADJUST, or EXPIRED)
            - quantity: int
            
        Optional Fields:
            - reason: str (alias for note)
            
        For specific operations, prefer dedicated endpoints:
        - Stock IN: POST /products/{id}/stock/in/
        - Stock OUT: POST /products/{id}/stock/out/
        
        Returns:
            Response: Created movement data
        """
        try:
            company = self.get_company()
            
            # Validate using the create serializer
            serializer = MovementCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get batch and validate it belongs to user's company
            batch_code = serializer.validated_data.get('batch_code')
            batch_id = serializer.validated_data.get('batch')
            
            if batch_code:
                try:
                    batch = Batch.objects.get(
                        code=batch_code,
                        product__company=company
                    )
                except Batch.DoesNotExist:
                    return Response(
                        {
                            "detail": "Lote no encontrado o no pertenece a tu empresa"
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            elif batch_id:
                try:
                    batch = Batch.objects.get(
                        id=batch_id,
                        product__company=company
                    )
                except Batch.DoesNotExist:
                    return Response(
                        {
                            "detail": "Lote no encontrado o no pertenece a tu empresa"
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {"detail": "Se requiere batch_code o batch"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            movement_type = serializer.validated_data.get('movement_type')
            quantity = serializer.validated_data.get('quantity')
            reason = serializer.validated_data.get('reason', '')
            
            # Handle different movement types
            try:
                if movement_type == 'OUT':
                    StockService.registrar_salida(
                        product=batch.product,
                        quantity=int(quantity),
                        note=reason
                    )
                elif movement_type == 'ADJUST':
                    StockService.ajustar_stock(
                        batch=batch,
                        new_quantity=int(quantity),
                        note=reason
                    )
                elif movement_type == 'EXPIRED':
                    StockService.marcar_vencido(batch)
                elif movement_type == 'IN':
                    # Direct IN movements are rare (usually via batch creation)
                    from inventario.models.movement import Movement
                    movement = Movement.objects.create(
                        batch=batch,
                        movement_type='IN',
                        quantity=int(quantity),
                        note=reason or 'Manual stock in'
                    )
                
                # Get the last created movement
                movement = batch.movements.latest('created_at')
                response_serializer = MovementSerializer(movement)
                return Response(
                    response_serializer.data,
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
        Delete movement (batch must belong to user's company).
        WARNING: This can affect stock calculations.
        
        Args:
            pk: Movement ID
            
        Returns:
            Response: Empty response with 204 status
        """
        try:
            company = self.get_company()
            
            movement = Movement.objects.filter(
                batch__product__company=company
            ).get(pk=pk)
            
            movement.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Movement.DoesNotExist:
            return Response(
                {"detail": "Movement not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as exc:
            return self.handle_exception(exc)
