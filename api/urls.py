from django.urls import path, include
from api.products.urls import urlpatterns as api_products_urls


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(api_products_urls)),
]