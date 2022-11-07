from django import forms
from django.contrib.auth import get_user_model


class SignUpModelForm(forms.ModelForm):
    error_messages = {'password_error': "The two password fields didn't match"}
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        required=True
    )
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
        fields = ('email', 'password1', 'password2',)

    def is_valid(self):
        if not self.errors:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 and password2 and password1 != password2:
                self.errors.update(self.error_messages)
        return super().is_valid()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
