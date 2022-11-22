import logging

import requests

logger = logging.getLogger(__name__)


class GetCurrencyBaseClient:
    base_url = None

    def _request(self, method: str,
                 params: dict = None,
                 headers: dict = None,
                 data: dict = None):
        try:
            response = requests.request(
                url=self.base_url,
                method=method,
                params=params or {},
                data=data or {},
                headers=headers or {}
            )
        except Exception as error:
            logger.error(error)
        else:
            return response.json()


class PrivatBankAPI(GetCurrencyBaseClient):
    """
         [
            {
            "ccy":"EUR",
            "base_ccy":"UAH",
            "buy":"19.20000",
            "sale":"20.00000"
            },
        ]
    :return: list
    """

    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def get_currency(self):
        currency_list = self._request(
            'GET',
            params={'exchange': '', 'json': '', 'coursid': 5}
        )
        for currency in currency_list:
            if 'err_internal_server_error' in currency.keys() or \
                    'err_incorrect_json' in currency.keys():
                mono = MonobankAPI()
                return mono.get_currency()
        return currency_list


class MonobankAPI(GetCurrencyBaseClient):
    """
    [
        {
            "currencyCodeA": 840,
            "currencyCodeB": 980,
            "date": 1552392228,
            "rateSell": 27,
            "rateBuy": 27.2,
            "rateCross": 27.1
        },
    ]
    :return: list
    """
    base_url = 'https://api.monobank.ua/bank/currency'

    def _reformat_currency(self):
        iso_codes = {
            980: 'UAH',
            840: 'USD',
            978: 'EUR'
        }
        currency_list = self._request(
            'GET',
            params={'json': ''}
        )
        reform_currency_list = []
        for currency in currency_list:
            if 'err_internal_server_error' in currency.keys() or \
                    'err_incorrect_json' in currency.keys() or \
                    'errorDescription' in currency.keys():
                nbu = NationalBankAPI()
                return nbu.get_currency()
            else:
                if iso_codes[currency['currencyCodeB']] == 'UAH' and \
                        currency['currencyCodeA'] in iso_codes.keys():
                    reform_currency_list.append({
                        'ccy': iso_codes[currency['currencyCodeA']],
                        'buy': currency['rateBuy'],
                        'sale': currency['rateSell']
                    })
        return reform_currency_list

    def get_currency(self) -> list:
        return self._reformat_currency()


class NationalBankAPI(GetCurrencyBaseClient):
    """
    [
        {
            "r030": 840,
            "txt": "Долар США",
            "rate":	36.5686,
            "cc": "USD",
            "exchangedate": "01.11.2022"
        },
    ]
    :return: list
    """
    base_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'

    def _reformat_currency(self):
        currency_list = self._request(
            'GET',
            params={'json': ''}
        )
        reform_currency_list = []
        for currency in currency_list:
            reform_currency_list.append({
                'ccy': currency['cc'],
                'buy': currency['rate'],
                'sale': currency['rate']
                })
        return reform_currency_list

    def get_currency(self) -> list:
        return self._reformat_currency()


pb_client = PrivatBankAPI()
