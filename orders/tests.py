from django.urls import reverse


def test_order_page(client, faker, login_user, product):
    url = reverse('shopping_cart')

    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)
    assert any(template.name == 'registration/login.html' for template in response.templates)

    client, user = login_user

    response = client.get(url)
    assert response.status_code == 200
    assert b'Shopping Cart' in response.content
    assert user == response.context_data['order'].user


def test_add_order(client, product, login_user):
    url = reverse('shopping_cart')
    client, user = login_user
    data = {
        'product_uuid': product.id
    }

    response = client.post(reverse('add_shopping_cart'), data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == url for i in response.redirect_chain)
    assert product in response.context_data['order'].products.all()


def test_delete_product_order(client, product, login_user):
    url = reverse('shopping_cart')
    client, user = login_user
    data = {
        'product_uuid': product.id
    }
    test_add_order(client, product, login_user)

    response = client.post(reverse('delete_shopping_cart'), data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == url for i in response.redirect_chain)
    assert not product in response.context_data['order'].products.all()


def test_clear_products_order(client, product, login_user):
    url = reverse('shopping_cart')
    client, user = login_user
    data = {
        'product_uuid': product.id
    }
    test_add_order(client, product, login_user)

    response = client.post(reverse('clear_shopping_cart'), data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('products') for i in response.redirect_chain)
    response = client.get(url)
    assert not response.context_data['order'].products.all()


def test_add_discount_order(client, faker, product, discount, login_user):
    url = reverse('shopping_cart')
    client, user = login_user
    data = {
        'code': discount.code
    }
    fake_data = {
        'code': faker.word()
    }
    test_add_order(client, product, login_user)

    response = client.post(reverse('discount_shopping_cart'), fake_data, follow=True)
    assert response.status_code == 200
    assert not response.context_data['order'].discount

    response = client.post(reverse('discount_shopping_cart'), data, follow=True)
    assert response.status_code == 200
    assert discount == response.context_data['order'].discount
    assert any(i[0] == url for i in response.redirect_chain)


def test_pay_order(client, product, faker, discount, login_user):
    url = reverse('shopping_cart')
    client, user = login_user

    test_add_discount_order(client, faker, product, discount, login_user)

    response = client.post(reverse('pay_shopping_cart'), follow=True)
    assert response.status_code == 200
    assert any(template.name == 'orders/successful_pay.html' for template in response.templates)

    response = client.get(url)
    assert response.status_code == 200
    assert response.context_data['order'].is_active
    assert not response.context_data['order'].is_paid
