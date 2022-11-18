#from pytest_mock import mocker

from currencies.models import CurrencyHistory
from currencies.tasks import get_currencies


#def test_get_currency_task(faker):
#    assert not CurrencyHistory.objects.exists()
#    get_currency = mocker.patch('currencies.cliens.cliens.pb_client.get_currency')
#    get_currency.return_value = [
#        {'ccy': 'USD', 'buy:': '2', 'sale':'3'},
#        {'ccy': 'EUR', 'buy:': '4', 'sale':'5'}]
#    assert not get_currency.call_count

#    get_currencies()
#    assert get_currency.call_count
#    assert CurrencyHistory.objects.filter(currency='USD', sale='3')
#    assert CurrencyHistory.objects.filter(currency='EUR', sale='5')
