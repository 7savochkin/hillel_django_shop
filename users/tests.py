import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.urls import reverse

from users.tasks import send_sms

User = get_user_model()


def test_registration_user_with_mail(client, faker):
    email = faker.email()
    phone = faker.phone_number()
    password = faker.password()
    url = reverse('sign_up')
    assert not User.objects.filter(email=email).exists()
    assert len(mail.outbox) == 0
    data = {
        'password1': password,
        'password2': password,
        'email': email,
        'phone': phone
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert User.objects.filter(email=email, is_active=False).exists()
    assert len(mail.outbox) == 1

    response = client.post(reverse('login'),
                           data={'email': email, 'password': password})
    assert response.status_code == 200

    uidb64, token = re.search("sign_up/(.*)/(.*)/",
                              mail.outbox[0].body).groups()

    response = client.get(reverse('sign_up_mail_confirm',
                                  args=(uidb64, token)))
    assert response.status_code == 302
    assert User.objects.filter(email=email, is_active=True).exists()

    response = client.post(reverse('login'),
                           data={'username': email, 'password': password})
    assert response.status_code == 302


def test_registration_user_with_phone(client, faker, cache_code):
    email = faker.email()
    phone = faker.phone_number()
    password = faker.password()
    url = reverse('sign_up')
    assert not User.objects.filter(email=email).exists()
    assert len(mail.outbox) == 0
    data = {
        'password1': password,
        'password2': password,
        'email': email,
        'phone': phone
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert User.objects.filter(phone=phone, is_active=False).exists()
    user = User.objects.get(phone=phone)
    response = client.post(reverse('sign_up_phone_confirm'), data={'code': cache_code}, follow=True)
    assert response.status_code == 200
    breakpoint()


def test_login_user(client, faker):
    url = reverse('login')
    email = faker.email()
    password = faker.password()
    phone = faker.phone_number()
    user = User.objects.create(
        email=email,
        first_name=email,
        phone=phone,
        is_phone_valid=True
    )
    user.set_password(password)
    user.save()
    # get login page
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'password': faker.password()
    }
    # post data login form
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][
               0] == 'Email ot phone number is required'

    data['username'] = faker.email()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][
               0] == 'Please enter a correct email address and password. Note that both fields may be case-sensitive.'

    del data['username']
    data['phone'] = faker.word()
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200

    data['username'] = email
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 302
