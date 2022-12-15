from django.urls import path, include

from api.products.views import ProductsViewSet

urlpatterns = [
    path('products/', ProductsViewSet.as_view())
]