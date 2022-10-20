from django.urls import path

from main.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('main/', MainView.as_view(), name='main'),
]
