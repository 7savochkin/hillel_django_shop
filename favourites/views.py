from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from favourites.forms import AddFavouritesForm, DeleteFavouritesForm
from favourites.mixins import GetFavouritesMixin
from products.forms import ProductFilterForm
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


class AddFavouritesView(GetFavouritesMixin, RedirectView):
    url = reverse_lazy('favourites')

    def post(self, request, *args, **kwargs):
        form = AddFavouritesForm(request.POST,
                                 favourites=self.get_favourites_object())
        if form.is_valid():
            messages.success(request, message='Product was add to favourites!')
            form.save()
        return self.get(request, *args, **kwargs)


class DeleteFavouritesView(GetFavouritesMixin, RedirectView):
    url = reverse_lazy('favourites')

    def post(self, request, *args, **kwargs):
        form = DeleteFavouritesForm(request.POST,
                                    favourites=self.get_favourites_object())
        if form.is_valid():
            messages.warning(request, message='Product was deleted!')
            form.save()
        return self.get(request, *args, **kwargs)
