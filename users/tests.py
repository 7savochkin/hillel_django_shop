from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def test_sign_up(client, faker):
    url = reverse('sign_up')
    email = faker.email()
    password = faker.password()
    phone = '+12125552368'
    data = {
        'email': faker.word(),
        'phone': faker.word(),
        'password1': password,
        'password2': faker.password()
    }

    response = client.get(url)

    assert response.status_code == 200
    assert any(template.name == 'registration/sign_up.html' for template in response.templates)

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert 'Enter a valid email address.' in response.content.decode()
    assert 'Enter a valid email address.' in response.context['form'].errors['email']

    data['email'] = email
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert 'Enter a valid phone number (e.g. +12125552368).' in response.content.decode()
    assert 'Enter a valid phone number (e.g. +12125552368).' in response.context['form'].errors['phone']

    data['phone'] = phone
    response = client.post(url, data=data)

    assert  response.status_code == 200
    assert "Passwords arent equal" in response.content.decode()
    assert 'Passwords arent equal' in response.context['form'].errors['__all__']

    data['password2'] = password
    response = client.post(url, data=data, follow=True)

    assert response.status_code == 200
    assert email == User.objects.all()[0].email
    assert any(template.name == 'main/index.html' for template in response.templates)


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
    assert response.context['form'].errors['__all__'][0] == 'Email ot phone number is required'

    data['username'] = faker.email()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Please enter a correct email address and password. Note that both fields may be case-sensitive.'

    del data['username']
    data['phone'] = faker.word()
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200

    data['username'] = email
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 302