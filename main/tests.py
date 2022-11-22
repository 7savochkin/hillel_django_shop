from django.urls import reverse
from django.core import mail


def test_main_page(client, faker):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200
    assert b'Our history' in response.content

    data = {
        'email': faker.word(),
        'text': faker.sentence()
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert not len(mail.outbox)

    data = {
        'email': faker.email(),
        'text': faker.sentence(),
    }
    response = client.post(url, data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == url for i in response.redirect_chain)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].from_email == data['email']
    assert mail.outbox[0].body == data['text']
