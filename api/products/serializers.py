from rest_framework import serializers

from products.models import Product, Category


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'actual_price', 'used',
                  'category', 'image', 'currency', 'sku',
                  'created_at', 'updated_at')
