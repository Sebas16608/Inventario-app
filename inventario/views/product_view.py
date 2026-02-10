from API import SuperApiView
from inventario.models.product import Product
from inventario.serializers import ProductSerializer

class ProductAPIView(SuperApiView):
    model = Product
    serializer_class = ProductSerializer
    filter_fields = ["name", "slug", "supplier"]
