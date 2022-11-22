from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(label='Email')
    text = forms.CharField(label='Text', widget=forms.Textarea())
