from django import forms

from items.models import Item


class ItemModelForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('name', 'description', 'image', 'category')
