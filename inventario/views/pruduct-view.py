from API import SuperApiView
from inventario.models.product import Product
from inventario.serializers import ProductSerializer

class ProductView(SuperApiView):
    model = Product
    serializer_class = ProductSerializer
    filter_fields = ["name", "slug", "supplier"]
