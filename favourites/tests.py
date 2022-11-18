from django.urls import reverse


def test_favourites_page(client, faker, login_user, product):
    url = reverse('favourites')

    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)
    assert any(template.name == 'registration/login.html' for template in response.templates)

    client, user = login_user

    response = client.get(url)
    assert response.status_code == 200
    assert b'Favourites' in response.content
    assert user == response.context_data['favourites'].user


def test_add_and_delete_favourites(client, faker, product, login_user):
    url = reverse('favourites')
    client, user = login_user
    data = {
        'product_uuid': product.id
    }
    fake_data = {
        'product_uuid': faker.uuid4()
    }

    response = client.post(reverse('add_favourites'), fake_data, follow=True)
    assert response.status_code == 200
    assert not product in response.context_data['favourites'].products.iterator()

    response = client.post(reverse('add_favourites'), data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == url for i in response.redirect_chain)
    assert product in response.context_data['favourites'].products.iterator()

    response = client.post(reverse('delete_favourites'), fake_data, follow=True)
    assert response.status_code == 200
    assert product in response.context_data['favourites'].products.iterator()

    response = client.post(reverse('delete_favourites'), data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == url for i in response.redirect_chain)
    assert not product in response.context_data['favourites'].products.iterator()
