from django.urls import path

from orders.views import AddShoppingCartView, ShoppingCartView, \
    DeleteShoppingCartView, ClearShoppingCartView, DiscountShoppingCartView, \
    PayShoppingCartView, successful_pay

urlpatterns = [
    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping_cart'),
    path('add/', AddShoppingCartView.as_view(), name='add_shopping_cart'),
    path('del/', DeleteShoppingCartView.as_view(), name='delete_shopping_cart'), # noqa
    path('clear/', ClearShoppingCartView.as_view(), name='clear_shopping_cart'), # noqa
    path('discount/', DiscountShoppingCartView.as_view(), name='discount_shopping_cart'),  # noqa
    path('pay/', PayShoppingCartView.as_view(), name='pay_shopping_cart'),
    path('successful_pay/', successful_pay, name='successful_pay'),
]
