from django.urls import path
from products.views import ProductView, export_csv, ImportCSVIntoProducts, \
    ProductDetail

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/csv/', export_csv, name='export_csv'),
    path('products/import_csv/', ImportCSVIntoProducts.as_view(), name='import_csv'), # noqa
    path('products/<uuid:pk>', ProductDetail.as_view(), name='product_detail'),
]
