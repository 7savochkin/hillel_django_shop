from django.urls import reverse

from products.models import Product


def test_product_page(client, product):
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'products/product_list.html' for template in response.templates)
    assert b'Our products:' in response.content
    assert product in response.context_data['object_list']


def test_product_detail(client, faker, login_user, product):
    url = reverse('products')
    response = client.get(url + faker.uuid4())
    assert response.status_code == 404

    response = client.get(url + str(product.id))
    assert response.status_code == 200
    assert any(template.name == 'products/product_detail.html' for template in response.templates)
    assert product.name.encode() in response.content

    client, user = login_user

    response = client.get(url + str(product.id))
    assert response.status_code == 200


def test_export_csv(client, product, login_user):
    url = reverse('export_csv')

    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)
    assert any(template.name == 'registration/login.html' for template in response.templates)

    client, user = login_user

    response = client.get(url)
    assert response.status_code == 200
    assert 'filename="products.csv"' in response.headers['Content-Disposition']
    assert all(product.name.encode() in response.content for product in Product.objects.iterator())
