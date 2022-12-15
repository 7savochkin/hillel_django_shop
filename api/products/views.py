from rest_framework.generics import ListAPIView

from api.products.serializers import ProductSerializer
from products.models import Product


class ProductsViewSet(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
