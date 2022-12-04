from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField


class SignUpModelForm(forms.ModelForm):
    error_messages = {'password_error': "The two password fields didn't match"}
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        required=True
    )
    phone = PhoneNumberField(
        label='Phone',
        required=True)
    password1 = forms.CharField(
        label='First password',
        widget=forms.PasswordInput(),
        required=True
    )
    password2 = forms.CharField(
        label='Second password ',
        widget=forms.PasswordInput(),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'phone', 'password1', 'password2',)

    def is_valid(self):
        if not self.errors:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 and password2 and password1 != password2:
                self.errors.update(self.error_messages)
        return super().is_valid()

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords arent equal")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_phone_valid = True
        if commit:
            user.save()
        return user


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
