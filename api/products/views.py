from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from api.products.filters import ProductFilter
from api.products.serializers import ProductsSerializer, CategoriesSerializer
from products.models import Product, Category


class ProductsViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ProductFilter


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='products',
            serializer_class=ProductsSerializer)
    def get_products(self, request, *args, **kwargs):
        category = self.get_object()
        products = category.product_set
        serializer = self.get_serializer(products, many=True)
        breakpoint()
        return Response(serializer.data)
