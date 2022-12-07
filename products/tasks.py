import decimal
import io
import logging

from celery import shared_task
from django.core.files.images import ImageFile

from currencies.models import CurrencyHistory
from products.client.client import products_parser
from products.models import Product, Category
from shop.api_clients import BaseClient
from shop.celery import app

logger = logging.getLogger(__name__)


@app.task
def saved_parsed_products(products_list: list):
    if not products_list:
        return
    request_client = BaseClient()
    for products_dict in products_list:
        category, _ = Category.objects.get_or_create(
            name=products_dict['category']
        )
        response = request_client.get_request(
            url=products_dict['image'],
            method='get')
        price = decimal.Decimal(
                ''.join(i for i in products_dict['price'] if i.isdigit()))
        actual_price = decimal.Decimal(
                ''.join(
                    (i for i in products_dict['actual_price'] if i.isdigit())))
        image = ImageFile(io.BytesIO(response), name='image.jpg')
        product, created = Product.objects.get_or_create(
            name=products_dict['name'],
            description=products_dict['description'],
            image=image,
            category=category,
            used=products_dict['used'],
            price=price,
            actual_price=actual_price,
            sku=products_dict['sku']
        )
        if not created:
            product.price = price
            product.actual_price = actual_price
            product.image = image
            product.save(update_fields=('price', 'actual_price', 'image'))


@app.task
def parse_products():
    saved_parsed_products.delay(products_parser.parse())


@shared_task
def update_currency_price():
    currency_list = CurrencyHistory.objects.order_by('-created_at').values(
        'currency', 'sale')[:2]
    for products in Product.objects.iterator():
        try:
            if products.currency == currency_list[0]['currency']:
                products.actual_price = products.price * currency_list[0][
                    'sale']
            elif products.currency == currency_list[1]['currency']:
                products.actual_price = products.price * currency_list[1][
                    'sale']
            else:
                products.actual_price = products.price
            products.save(update_fields=['actual_price'])
        except (KeyError, ValueError) as error:
            logger.error(error)
