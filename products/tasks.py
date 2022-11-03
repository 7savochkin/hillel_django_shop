from celery import shared_task

from currencies.models import CurrencyHistory
from products.models import Product


@shared_task
def update_currency_price():
    currency_list = CurrencyHistory.objects.order_by('-created_at').values(
        'currency', 'sale')[:2]
    for products in Product.objects.iterator():
        if products.currency == currency_list[0]['currency']:
            products.actual_price = products.price * currency_list[0]['sale']
        elif products.currency == currency_list[1]['currency']:
            products.actual_price = products.price * currency_list[1]['sale']
        else:
            products.actual_price = products.price
        products.save(update_fields=['actual_price'])
