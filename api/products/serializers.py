from rest_framework import serializers

from products.models import Product


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description')


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'