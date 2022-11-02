import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from currencies.clients.client import pb_client
from currencies.models import CurrencyHistory
from shop.celery import app
from shop.model_choices import Currency

logger = logging.getLogger(__name__)


@app.task
def clear_old_currencies():
    CurrencyHistory.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=3)
    ).delete()


@shared_task
def get_currencies():
    currency_list = pb_client.get_currency()
    currency_history_list = []
    for currency in currency_list:
        try:
            if currency['ccy'] in [elem.value for elem in Currency]:
                currency_history_list.append(
                    CurrencyHistory(currency=currency['ccy'],
                                    buy=currency['buy'],
                                    sale=currency['sale']
                                    )
                )
        except (KeyError, ValueError) as error:
            logger.error(error)
    if currency_history_list:
        CurrencyHistory.objects.bulk_create(currency_history_list)
        clear_old_currencies.delay()
