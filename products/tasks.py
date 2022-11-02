from celery import shared_task
from django.utils import timezone

from currencies.models import CurrencyHistory
from products.models import Product


@shared_task
def update_currency_price():
    usd = CurrencyHistory.objects.filter(currency='USD',
                                         created_at__lt=timezone.now()).first()
    for products in Product.objects.all():
        products.actual_price = products.price * usd.buy
        products.save()
