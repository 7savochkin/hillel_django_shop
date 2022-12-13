import random

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField, \
    UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from shop import settings
from shop.helpers import send_html_mail
from users.tasks import send_sms

User = get_user_model()


class SignUpModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone")
        field_classes = {'email': UsernameField}

    def clean(self):
        self.instance.is_active = False
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        context = {
            'email': user.email,
            'domain': settings.DOMAIN,
            'site_name': 'SHOP',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'subject': 'Confirm registration'
        }
        subject_template_name = 'emails/sign_up/sign_up_confirm_subject.txt'  # noqa
        email_template_name = 'emails/sign_up/sign_up_confirm_email.html'  # noqa
        send_html_mail(
            subject_template_name,
            email_template_name,
            from_email=settings.SERVER_EMAIL,
            to_email=user.email,
            context=context
        )

        if self.cleaned_data.get('phone'):
            code = random.randint(10000, 99999)
            cache.set(f'{str(user.id)}_code', code, timeout=60)
            send_sms.delay(self.cleaned_data.get('phone'), code)
        return user


class SignUpPhoneConfirmForm(forms.Form):
    code = forms.IntegerField(min_value=10000, max_value=99999)

    def is_valid(self, session_user_id=None):
        if not self.errors:
            cache_code = cache.get(f'{str(session_user_id)}_code')
            input_code = self.cleaned_data['code']
            if cache_code == input_code:
                return True
            else:
                self.errors.update({'code error': 'Please, write valid code'})
                return False

    def save(self, session_user_id=None):
        user = User.objects.get(id=session_user_id)
        user.is_active = True
        user.is_phone_valid = True
        return user.save()


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             required=False)
    phone = forms.CharField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        phone = self.cleaned_data.get('phone')

        if not username and not phone:
            raise ValidationError('Email ot phone number is required')
        if password:
            kwargs = {'password': password, 'username': username}
            if phone and not username:
                kwargs.pop('username')
                kwargs.update({'phone': phone})
            self.user_cache = authenticate(self.request, **kwargs)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
