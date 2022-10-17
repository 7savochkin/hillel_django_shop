from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView

from users.forms import SignUpModelForm


class SignUpView(TemplateView):
    template_name = 'registration/sign_up.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': kwargs.get('form') or SignUpModelForm})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        form = form(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('/main/')
        return self.get(request, form=form, *args, **kwargs)
