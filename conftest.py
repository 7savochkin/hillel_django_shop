import csv
import os

import factory
import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from faker import Faker
from pytest_factoryboy import register

from orders.models import Discount
from products.models import Category, Product
from shop.constants import DECIMAL_PLACES

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
def product(db):
    category = Category.objects.create(
        name=fake.word()
    )
    product = Product.objects.create(
        name=fake.word(),
        category=category
    )
    yield product


@pytest.fixture(scope='function')
def test_file(db):
    category = Category.objects.create(
        name=fake.word()
    )
    with open('test.csv', 'w') as file:
        fieldnames = ['name', 'category', 'description', 'price', 'sku']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'name': fake.name(),
            'category': category.name,
            'description': fake.sentence(),
            'price': fake.pydecimal(
                min_value=1,
                left_digits=DECIMAL_PLACES,
                right_digits=DECIMAL_PLACES,
            ),
            'sku': fake.word(),
        })
    with open('test.csv', 'r') as file:
        yield file
    os.remove(os.getcwd() + '/test.csv')


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


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda x: fake.email())
    first_name = factory.Sequence(lambda x: fake.name())
    last_name = factory.Sequence(lambda x: fake.name())


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda x: fake.email())
    description = factory.Sequence(lambda x: fake.sentence())
    image = factory.django.ImageField()


@register
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda x: fake.word())
    description = factory.Sequence(lambda x: fake.sentence())
    image = factory.django.ImageField()
    price = factory.Sequence(lambda x: fake.pydecimal(
        min_value=1,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))
    sku = factory.Sequence(lambda x: fake.word())
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def post_create(self, created, *args, **kwargs):
        if created and not kwargs.get('deny_post'):
            for _ in range(1, 3):
                self.products.add(
                    ProductFactory(post_create__deny_post=True)
                )


@pytest.fixture(scope='function')
def login_user(db):
    phone = '+380971778402'
    password = '380971778402'
#    user, _ = User.objects.get_or_create(
#        email='user@user.com',
#        first_name='John Smith',
#        phone='+380971778402',
#        is_phone_valid=True
#    )
    user = UserFactory(phone=phone, is_phone_valid=True)
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'),
                           data={'phone': phone, 'password': password})

    assert response.status_code == 302
    yield client, user


@pytest.fixture(scope='function')
def login_staff_user(db):
    phone = '+380971778404'
    password = '380971778404'
    user = UserFactory(phone=phone, is_phone_valid=True, is_staff=True)
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'),
                           data={'phone': phone, 'password': password})

    assert response.status_code == 302
    yield client, user
