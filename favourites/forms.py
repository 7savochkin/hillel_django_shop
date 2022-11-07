from django import forms

from products.models import Product


class BaseFavouriteForm(forms.Form):
    product_uuid = forms.UUIDField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.favourites = kwargs['favourites']

    def is_valid(self):
        if not self.errors:
            try:
                Product.objects.get(id=self.cleaned_data['product_uuid'])
            except Product.DoesNotExist:
                self.errors.update({
                    'product_error': 'Not valid uuid'
                })
        return super().is_valid()


class AddFavouritesForm(BaseFavouriteForm):
    def save(self):
        self.favourites.products.add(
            Product.objects.get(id=self.cleaned_data['product_uuid']))
        return self.favourites.save()


class DeleteFavouritesForm(BaseFavouriteForm):
    def save(self):
        self.favourites.products.remove(
            Product.objects.get(id=self.cleaned_data['product_uuid']))
        return self.favourites.save()
