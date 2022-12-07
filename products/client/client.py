import logging

from bs4 import BeautifulSoup

from shop.api_clients import BaseClient


logger = logging.getLogger(__name__)


class Parser(BaseClient):
    base_url = 'https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&body.id[0]=3&categories.main.id=1&brand.id[0]=9&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=0&size=10' # noqa

    def parse(self):
        response = self.get_request(method='get')
        soup = BeautifulSoup(response)
        try:
            all_categories = soup.find(
                'div', attrs={'id': 'bodyBlock'}).find(
                'div', attrs={'class': "more-checkbox"}).text.split()
            filter_tags = soup.find_all(
                'span', attrs={'class': "tagging-filter small"})
            for tag in filter_tags:
                clear_tag = tag.text.split('×')[0].strip()
                if clear_tag in iter(all_categories):
                    category_name = clear_tag
                else:
                    category_name = 'No category'
        except (AssertionError, IndexError) as error:
            logger.error(error)
        else:
            product_list = []
            ticket_items = soup.find_all(
                'section', attrs={'class': "ticket-item"})
            for item in ticket_items:
                try:
                    name = item.find(
                        'div', attrs={
                            'class': "item ticket-title"}).text.strip()
                    description = item.find(
                        'div', attrs={'class': "definition-data"}).find(
                        'p').text.strip()
                    price = item.find(
                        'span', attrs={'data-currency': "USD"}).text.strip()
                    actual_price = item.find(
                        'span', attrs={'data-currency': "UAH"}).text.strip()
                    image_url = item.find('picture').find('img').attrs['src']
                    sku = item.attrs['data-advertisement-id']
                    product_list.append({
                        'name': name,
                        'description': description,
                        'category': category_name,
                        'image': image_url,
                        'price': price,
                        'actual_price': actual_price,
                        'sku': sku,
                        'used': True
                    })
                except (AssertionError, KeyError) as error:
                    logger.error(error)
            return product_list


products_parser = Parser()
