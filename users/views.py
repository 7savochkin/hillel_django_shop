from django.contrib.auth import login
from django.views.generic import TemplateView

from users.forms import LoginForm


# todo remove
class LoginView(TemplateView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': kwargs.get('form') or LoginForm})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        form = form(request.POST)
        if form.is_valid():
            login(request, form.user)
        return self.get(request, form=form, *args, **kwargs)
