from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe

from shop.mixins.models_mixins import PrimaryKeyMixin


class Item(PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/item')
    category = models.ForeignKey(
        'items.Category',
        on_delete=models.CASCADE)

    def view_item_image(self):
        if self.image:
            return mark_safe((
                '<img src="{}" width="100" height="100" />'.format(
                    self.image.url)))
        return ''

    def __str__(self):
        return f'{self.name}'


class Category(PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/category')

    def __str__(self):
        return f'{self.name} | {self.description}'


class Product(PrimaryKeyMixin):
    price = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    sku = models.CharField(
        max_length=64,
        blank=True,
        null=True)
    item = models.ManyToManyField(Item)

    def __str__(self):
        return f"{self.sku} | {self.price}"
