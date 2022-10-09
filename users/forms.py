from django import forms
from django.contrib.auth import authenticate


# todo remove
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def is_valid(self):
        if not self.errors:
            self.user = authenticate(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
            if not self.user:
                self.errors.update({'user': 'Wrong username or password'})
        return super().is_valid()
