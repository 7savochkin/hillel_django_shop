from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    price__gte = filters.NumberFilter(field_name='price',
                                      lookup_expr='gte')
    price__lte = filters.NumberFilter(field_name='price',
                                      lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'category__name', 'currency', 'price', 'used']
