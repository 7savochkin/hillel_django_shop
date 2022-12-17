from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from api.products.serializers import ProductsSerializer,\
    ProductRetrieveSerializer
from products.models import Product


class ProductsViewSet(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]


class ProductDetailViewSet(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer
    permission_classes = [IsAuthenticated]