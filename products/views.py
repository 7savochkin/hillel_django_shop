from django.views.generic import ListView

from products.models import Product


class ProductView(ListView):
    model = Product
