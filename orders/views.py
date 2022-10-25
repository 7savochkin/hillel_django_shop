from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from orders.forms import AddShoppingCartForm, DeleteShoppingCartForm, \
    DiscountShoppingCartForm
from orders.models import Order


class BaseShoppingCartRedirectView(RedirectView):
    url = reverse_lazy('shopping_cart')

    def post(self, request, *args, **kwargs):
        self.order = Order.objects.get_or_create(is_active=True,  # noqa
                                                 is_paid=False,
                                                 user=self.request.user)[0]
        return self.get(request, *args, **kwargs)


class ShoppingCartView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/shopping_cart_view.html'

    def get_context_data(self, **kwargs):
        context = super(ShoppingCartView, self).get_context_data()
        context.update({
            'order': Order.objects.get_or_create(is_active=True,
                                                 is_paid=False,
                                                 user=self.request.user)[0]
        })
        return context


class AddShoppingCartView(BaseShoppingCartRedirectView):
    url = reverse_lazy('products')

    def post(self, request, *args, **kwargs):
        super(AddShoppingCartView, self).post(request, *args, *kwargs)
        form = AddShoppingCartForm(request.POST, order=self.order)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)


class DeleteShoppingCartView(BaseShoppingCartRedirectView):

    def post(self, request, *args, **kwargs):
        super(DeleteShoppingCartView, self).post(request, *args, *kwargs)
        form = DeleteShoppingCartForm(request.POST, order=self.order)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)


class ClearShoppingCartView(BaseShoppingCartRedirectView):
    url = reverse_lazy('products')

    def post(self, request, *args, **kwargs):
        super(ClearShoppingCartView, self).post(request, *args, *kwargs)
        self.order.delete()
        return self.get(request, *args, **kwargs)


class DiscountShoppingCartView(BaseShoppingCartRedirectView):

    def post(self, request, *args, **kwargs):
        super(DiscountShoppingCartView, self).post(request, *args, *kwargs)
        form = DiscountShoppingCartForm(request.POST, order=self.order)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)


class PayShoppingCartView(BaseShoppingCartRedirectView):
    url = reverse_lazy('successful_pay')

    def post(self, request, *args, **kwargs):
        super(PayShoppingCartView, self).post(request, *args, *kwargs)
        if self.order.products.exists():
            self.order.is_active, self.order.is_paid = self.order.is_paid, self.order.is_active # noqa
            self.order.save()
        return self.get(request, *args, **kwargs)


def successful_pay(request, *args, **kwargs):
    return render(request, template_name='orders/successful_pay.html')
