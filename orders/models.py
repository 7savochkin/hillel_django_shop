from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, \
    BEFORE_SAVE

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PrimaryKeyMixin
from shop.model_choices import DiscountTypes


class Discount(PrimaryKeyMixin):
    amount = models.DecimalField(max_digits=MAX_DIGITS,
                                 decimal_places=DECIMAL_PLACES,
                                 default=0)
    code = models.CharField(
        max_length=30)
    is_active = models.BooleanField(
        default=True)
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE)

    def __str__(self):
        return f'{self.code} | {self.amount} | {self.is_active}'


class Order(LifecycleModelMixin, PrimaryKeyMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    products = models.ManyToManyField("products.Product")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    def get_discount_total_amount(self):
        if self.discount:
            if self.products.exists():
                if self.discount.discount_type == DiscountTypes.VALUE:
                    self.total_amount -= self.discount.amount
                else:
                    self.total_amount -= (
                            self.total_amount / 100 * self.discount.amount).quantize(
                        # noqa
                        Decimal('.01'))
        return self.total_amount

    @hook(BEFORE_SAVE)
    def order_after_save(self):
        self.total_amount = 0
        for product in self.products.all():
            self.total_amount += product.price

    @hook(AFTER_UPDATE)
    def order_after_update(self):
        if self.discount:
            self.total_amount = self.get_discount_total_amount()
            self.save(update_fields=('total_amount',), skip_hooks=True)
