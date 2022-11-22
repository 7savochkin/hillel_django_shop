import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView

from products.forms import ImportForm
from products.models import Product
from shop.mixins.views_mixins import StaffUserCheck
from shop.settings import DOMAIN


class ProductView(ListView):
    model = Product

    def get_queryset(self):
        query_set = super(ProductView, self).get_queryset()
        query_set = query_set.select_related('category').prefetch_related(
            'products__products')
        return self.model.get_products() and query_set


class ProductDetail(DetailView):
    model = Product


@login_required
def export_csv(request, *args, **kwargs):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="products.csv"'}
    )
    fieldnames = ['name', 'category', 'description', 'price', 'sku', 'image']
    writer = csv.DictWriter(response, fieldnames=fieldnames)

    writer.writeheader()
    for product in Product.objects.iterator():
        writer.writerow({
            'name': product.name,
            'category': product.category.name,
            'description': product.description,
            'price': product.price,
            'sku': product.sku,
            'image': DOMAIN + product.image.url
        })
    return response


class ImportCSVIntoProducts(StaffUserCheck, FormView):
    template_name = 'products/import_csv.html'
    form_class = ImportForm
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
