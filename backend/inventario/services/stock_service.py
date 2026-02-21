from django.db import transaction
from inventario.models.batch import Batch
from inventario.models.movement import Movement


class StockService:

    @staticmethod
    def _generate_batch_code(company_id):
        last_batch = Batch.objects.filter(product__company_id=company_id).order_by('-id').first()
        if last_batch and last_batch.code:
            try:
                last_num = int(last_batch.code.split('-')[-1])
                new_num = last_num + 1
            except (ValueError, IndexError):
                new_num = 1
        else:
            new_num = 1
        return f"LOTE-{company_id}-{new_num:04d}"

    @staticmethod
    @transaction.atomic
    def registrar_entrada(
        product,
        quantity,
        purchase_price,
        expiration_date,
        supplier,
        code=None
    ):
        if not code:
            code = StockService._generate_batch_code(product.company_id)
        
        batch = Batch.objects.create(
            product=product,
            quantity_received=quantity,
            quantity_available=quantity,
            purchase_price=purchase_price,
            expiration_date=expiration_date,
            supplier=supplier,
            code=code
        )

        Movement.objects.create(
            batch=batch,
            movement_type="IN",
            quantity=quantity,
            note="Ingreso de producto"
        )

        return batch
    
    @staticmethod
    @transaction.atomic
    def registrar_salida(product, quantity, note=None):
        batches = (
            Batch.objects
            .filter(product=product, quantity_available__gt=0)
            .order_by("expiration_date", "id")
        )

        total = sum(b.quantity_available for b in batches)
        if total < quantity:
            raise ValueError("Stock insuficiente")

        restante = quantity

        for batch in batches:
            if restante == 0:
                break

            if batch.quantity_available >= restante:
                batch.quantity_available -= restante
                batch.save()

                Movement.objects.create(
                    batch=batch,
                    movement_type="OUT",
                    quantity=restante,
                    note=note
                )
                restante = 0
            else:
                usado = batch.quantity_available
                batch.quantity_available = 0
                batch.save()

                Movement.objects.create(
                    batch=batch,
                    movement_type="OUT",
                    quantity=usado,
                    note=note
                )
                restante -= usado

    @staticmethod
    @transaction.atomic
    def ajustar_stock(batch, new_quantity, note=None):
        diferencia = new_quantity - batch.quantity_available
        batch.quantity_available = new_quantity
        batch.save()

        Movement.objects.create(
            batch=batch,
            movement_type="ADJUST",
            quantity=abs(diferencia),
            note=note or "Ajuste manual"
        )

    @staticmethod
    @transaction.atomic
    def marcar_vencido(batch):
        if batch.quantity_available <= 0:
            return

        cantidad = batch.quantity_available
        batch.quantity_available = 0
        batch.save()

        Movement.objects.create(
            batch=batch,
            movement_type="EXPIRED",
            quantity=cantidad,
            note="Producto vencido"
        )

def stock_total(product):
    return sum(
        b.quantity_available
        for b in product.batches.all()
    )
