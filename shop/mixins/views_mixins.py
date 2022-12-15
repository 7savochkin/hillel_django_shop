from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView


class StaffUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff


class ProductFilterMixin(TemplateView):
    filter_form = None
    queryset = None

    def filtered_object_list(self, queryset):
        category_id = self.request.GET.get('category')
        currency = self.request.GET.get('currency')
        name = self.request.GET.get('name')
        if category_id:
            queryset = queryset.filter(category=category_id)
        if currency:
            queryset = queryset.filter(currency=currency)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        filtered_queryset = self.filtered_object_list(self.queryset)
        page_number = self.request.GET.get('page')
        paginator = Paginator(filtered_queryset, 2)
        pages = paginator.get_page(page_number)
        context_data.update({'object_list': pages})
        context_data.update({'filter_form': self.filter_form})
        return context_data
