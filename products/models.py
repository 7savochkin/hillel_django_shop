from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, \
    AFTER_DELETE, AFTER_SAVE

from currencies.models import CurrencyHistory  # noqa
from shop.constants import DECIMAL_PLACES, MAX_DIGITS
from shop.mixins.models_mixins import PrimaryKeyMixin
from shop.model_choices import Currency


class Product(LifecycleModelMixin, PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/product',
                              default='static/images/products/no_image.jpg')
    category = models.ForeignKey(
        'products.Category',
        on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    actual_price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )
    sku = models.CharField(
        max_length=64,
        blank=True,
        null=True)
    products = models.ManyToManyField('products.Product', blank=True)

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def _cache_key(cls):
        return 'products'

    @classmethod
    def get_products(cls):
        products = cache.get(cls._cache_key())
        if not products:
            products = Product.objects.all()
            cache.set(cls._cache_key(), products)
        return products

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clear_products_cache(self):
        cache.delete(self._cache_key())


class Category(PrimaryKeyMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/category')

    def __str__(self):
        return f'{self.name} | {self.description}'




