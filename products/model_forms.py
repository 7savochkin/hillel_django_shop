from django import forms

from products.models import Item


class ItemModelForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name', 'description', 'image', 'category')
