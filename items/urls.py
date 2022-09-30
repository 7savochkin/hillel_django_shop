from django.urls import path
from items.views import items

urlpatterns = [
    path('items/', items, name='items'),
]
