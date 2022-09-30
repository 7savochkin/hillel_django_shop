from django.core.validators import MinValueValidator
from django.db import models

from shop.mixins.models_mixins import PrimaryKeyMixin


class Item(PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/item')
    category = models.ForeignKey(
        'items.Category',
        on_delete=models.CASCADE)


class Category(PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/category')


class Product(PrimaryKeyMixin):
    price = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    sku = models.CharField(
        max_length=64,
        blank=True,
        null=True)
    item = models.ManyToManyField(Item)
