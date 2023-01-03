import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from django_filters.views import FilterView

from products.filters import ProductFilter
from products.forms import ImportForm
from products.models import Product
from shop.mixins.views_mixins import StaffUserCheck
from shop.settings import DOMAIN


class ProductView(FilterView):
    model = Product
    paginate_by = 4
    filterset_class = ProductFilter
    template_name_suffix = '_list'

    def get_queryset(self):
        qs = self.model.get_products().filter(used=False)
        return qs


class ProductDetail(DetailView):
    model = Product


class ProductUsedView(FilterView):
    model = Product
    paginate_by = 4
    filterset_class = ProductFilter
    template_name_suffix = '_list'

    def get_queryset(self):
        qs = self.model.get_products().filter(used=True)
        return qs


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
