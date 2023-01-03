from django.urls import path, include
from rest_framework.authtoken import views

from api.feedbacks.urls import urlpatterns as api_feedbacks_urls
from api.products.urls import urlpatterns as api_products_urls

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(api_products_urls)),
    path('api/v1/', include(api_feedbacks_urls)),
]
