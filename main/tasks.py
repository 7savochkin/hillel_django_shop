from django.core.mail import mail_managers, send_mail

from config.models import Config
from shop.celery import app


@app.task
def send_contact_form(email, text):
    send_mail(
        'BMW Compnay - Contact Form',
        text,
        email,
        [Config.load().contact_form_email]
    )