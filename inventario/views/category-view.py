from inventario.models import Category
from inventario.serializers import CategorySerializer
from API import SuperApiView

class CategoryAPIView(SuperApiView):
    model = Category
    serializer_class = CategorySerializer
    filter_fields = ['name', 'slug'] 
