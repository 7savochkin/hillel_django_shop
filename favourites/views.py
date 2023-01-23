from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, DetailView

from favourites.forms import DeleteFavouritesForm
from favourites.mixins import GetFavouritesMixin
from products.forms import ProductFilterForm
from products.models import Product
from shop.decorators import ajax_required
from shop.mixins.views_mixins import ProductFilterMixin


class FavouritesView(LoginRequiredMixin, GetFavouritesMixin,
                     ProductFilterMixin):
    template_name = 'favourites/product_favourite.html'
    filter_form = ProductFilterForm

    def _default_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = self._default_context_data(**kwargs)
        self.queryset = self.get_favourites_object()
        filtered_queryset = self.filtered_object_list(
            queryset=self.queryset.products.all()
        )
        context_data.update({'object_list': filtered_queryset})
        context_data.update({'filter_form': self.filter_form})
        return context_data


class AddOrDeleteFavouritesView(GetFavouritesMixin, DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        favourites = self.get_favourites_object()
        product = self.get_object()
        if product not in favourites.products.all():
            favourites.products.add(product)
            favourites.save()
            messages.success(request,
                             message='Product was added to favourites!')
        else:
            messages.warning(request,
                             message='Product was deleted from favourite')
            favourites.products.remove(product)
            favourites.save()
        return HttpResponseRedirect(reverse_lazy('products') + str(product.id))


class AJAXAddOrDeleteFavouritesView(GetFavouritesMixin, DetailView):
    model = Product

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        favourites = self.get_favourites_object()
        product = self.get_object()
        if product not in favourites.products.all():
            favourites.products.add(product)
            favourites.save()
        else:
            favourites.products.remove(product)
            favourites.save()
        attached = product in favourites.products.all()
        return JsonResponse(data={'attached': attached})


class DeleteFavouritesView(GetFavouritesMixin, RedirectView):
    url = reverse_lazy('favourites')

    def post(self, request, *args, **kwargs):
        form = DeleteFavouritesForm(request.POST,
                                    favourites=self.get_favourites_object())
        if form.is_valid():
            messages.warning(request, message='Product was deleted!')
            form.save()
        return self.get(request, *args, **kwargs)
