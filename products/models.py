from django.core.validators import MinValueValidator
from django.db import models

from shop.mixins.models_mixins import PrimaryKeyMixin


class Product(PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/product')
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    sku = models.CharField(
        max_length=64,
        blank=True,
        null=True)
    products = models.ManyToManyField('products.Product', blank=True)

    def __str__(self):
        return f'{self.name}'


class Category(PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/category')

    def __str__(self):
        return f'{self.name} | {self.description}'
