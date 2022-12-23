"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.urls import urlpatterns as api_urls
from favourites.urls import urlpatterns as favourites_urls
from feedbacks.urls import urlpatterns as feedbacks_urls
from main.urls import urlpatterns as main_urls
from orders.urls import urlpatterns as orders_urls
from products.urls import urlpatterns as products_urls
from users.urls import urlpatterns as users_urls

schema_view = get_schema_view(
    openapi.Info(
        title="BMW Store API",
        default_version='v1',
        description="It's api for working with database.",
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(products_urls)),
    path('', include(feedbacks_urls)),
    path('', include(users_urls)),
    path('', include(main_urls)),
    path('', include(orders_urls)),
    path('', include(favourites_urls)),
    path('', include(api_urls)),
    re_path(r'^api/v1/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api/v1/swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^api/v1/docs/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
