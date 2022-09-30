from django.contrib.auth import get_user_model
from django.db import models

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PrimaryKeyMixin
from shop.model_choices import DiscountTypes


class Discount(PrimaryKeyMixin):
    amount = models.PositiveIntegerField(
        default=0)
    code = models.CharField(
        max_length=30)
    is_active = models.BooleanField(
        default=True)
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE)


class Order(PrimaryKeyMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    products = models.ManyToManyField('items.Product')
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        blank = True,
        null= True,
    )
