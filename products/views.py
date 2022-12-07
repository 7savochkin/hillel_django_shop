import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, TemplateView

from products.forms import ImportForm
from products.models import Product
from shop.mixins.views_mixins import StaffUserCheck
from shop.settings import DOMAIN


class ProductView(TemplateView):
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context_data = super(ProductView, self).get_context_data(**kwargs)
        used_products = [product for product in Product.objects.select_related(
            'category').prefetch_related(
            'products__products').iterator()
                         if not product.used]
        context_data.update({'object_list': used_products})
        return context_data


class ProductDetail(DetailView):
    model = Product


class ProductUsedView(TemplateView):
    template_name = 'products/product_used.html'

    def get_context_data(self, **kwargs):
        context_data = super(ProductUsedView, self).get_context_data(**kwargs)
        used_products = [product for product in Product.objects.select_related(
            'category').prefetch_related(
            'products__products').iterator()
                         if product.used]
        context_data.update({'used_products': used_products})
        return context_data


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
