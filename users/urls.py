from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import SignUpView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
