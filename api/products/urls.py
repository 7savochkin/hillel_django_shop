from django.urls import path

from api.products.views import ProductsViewSet, ProductDetailViewSet

urlpatterns = [
    path('products/', ProductsViewSet.as_view()),
    path('products/<uuid:pk>', ProductDetailViewSet.as_view())
]
