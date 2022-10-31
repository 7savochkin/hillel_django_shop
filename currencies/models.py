from django.db import models

from shop.constants import DECIMAL_PLACES, MAX_DIGITS
from shop.mixins.models_mixins import PrimaryKeyMixin
from shop.model_choices import Currency


class CurrencyHistory(PrimaryKeyMixin):
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sale = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )

    def __str__(self):
        return f'{self.currency} | {self.created_at} |{self.buy} | {self.sale}'
