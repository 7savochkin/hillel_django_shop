from django import forms

from orders.models import Discount
from products.models import Product


class BaseShoppingCartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.order = kwargs['order']


class AddShoppingCartForm(BaseShoppingCartForm):
    product_uuid = forms.UUIDField(
        required=True
    )

    def save(self):
        product = Product.objects.get(id=self.cleaned_data['product_uuid'])
        self.order.products.add(product)
        return self.order.save()


class DeleteShoppingCartForm(BaseShoppingCartForm):
    product_uuid = forms.UUIDField(
        required=True
    )

    def save(self):
        product = Product.objects.get(id=self.cleaned_data['product_uuid'])
        self.order.products.remove(product)
        return self.order.save()


class DiscountShoppingCartForm(BaseShoppingCartForm):
    code = forms.CharField(max_length=30)

    def is_valid(self):
        if not self.errors:
            try:
                discount = Discount.objects.get(code=self.cleaned_data['code'])
                if not discount.is_active:
                    raise Discount.DoesNotExist
            except Discount.DoesNotExist:
                self.errors.update({
                    'discount_error': 'Please write valid discount'
                })
        return super().is_valid()

    def save(self):
        discount = Discount.objects.get(code=self.cleaned_data['code'])
        self.order.discount = discount
        return self.order.save()
