from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import SignUpView, LoginView, SignUpPhoneConfirm, \
    SignUpEmailConfirm

#    SignUpEmailConfirm

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('sign_up/phoneconfirm/', SignUpPhoneConfirm.as_view(),
         name='sign_up_phone_confirm'),
    path('sign_up/<uidb64>/<token>/', SignUpEmailConfirm.as_view(),
         name='sign_up_mail_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
