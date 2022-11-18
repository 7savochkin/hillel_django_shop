import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.client import Client
from faker import Faker

from orders.models import Discount
from products.models import Category, Product

fake = Faker()
User = get_user_model()


@pytest.fixture(scope='session')
def faker():
    # global fake
    yield fake


@pytest.fixture(scope='function')
def user(db):
    user, _ = User.objects.get_or_create(
        email='user@user.com',
        first_name='John Smith',
        phone='+380971778402',
        is_phone_valid=True
    )
    user.set_password('380971778402')
    user.save()
    yield user


@pytest.fixture(scope='function')
def login_user(db):
    phone = '+380971778402'
    password = '380971778402'
    user, _ = User.objects.get_or_create(
        email='user@user.com',
        first_name='John Smith',
        phone='+380971778402',
        is_phone_valid=True
    )
    user.set_password('380971778402')
    user.save()
    client = Client()
    response = client.post(reverse('login'),
                           data={'phone': phone, 'password': password})

    assert response.status_code == 302
    yield client, user


@pytest.fixture(scope='function')
def product(db):
    category = Category.objects.create(
        name='Coupe'
    )
    product = Product.objects.create(
        name='2022 BMW M3',
        category=category
    )
    yield product


@pytest.fixture(scope='function')
def discount(db):
    discount = Discount.objects.create(
        code='shop'
    )
    yield discount


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    from pprint import pp
    __builtins__['pp'] = pp
    # code before tests run
    yield
    del __builtins__['pp']
    # code after tests run
