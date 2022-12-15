import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView

from products.forms import ImportForm, ProductFilterForm
from products.models import Product
from shop.mixins.views_mixins import StaffUserCheck, ProductFilterMixin
from shop.settings import DOMAIN


class ProductView(ProductFilterMixin):
    template_name = 'products/product_list.html'
    filter_form = ProductFilterForm
    queryset = Product.get_products().filter(used=False)


class ProductDetail(DetailView):
    model = Product


class ProductUsedView(ProductFilterMixin):
    template_name = 'products/product_used.html'
    filter_form = ProductFilterForm
    queryset = Product.get_products().filter(used=True)


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
