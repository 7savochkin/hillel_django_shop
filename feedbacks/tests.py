from django.urls import reverse


def test_feedbacks(client, faker, login_user):
    url = reverse('feedbacks')
    text = faker.sentence()
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)
    assert any(template.name == 'registration/login.html' for template in response.templates)

    client, user = login_user

    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'feedbacks/index.html' for template in response.templates)
    assert b'Feedbacks' in response.content

    data = {
        'text': text,
        'rating': 7,
        'user': str(user.id)
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['rating'][0] == 'Ensure this value is less than or equal to 5.'

    data['rating'] = 4
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert text.encode() in response.content
