from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import FormView
from django.contrib.auth.views import LoginView as AuthLoginView

from shop.settings import AUTHENTICATION_BACKENDS

from users.forms import SignUpModelForm, CustomAuthenticationForm


class SignUpView(FormView):
    template_name = 'registration/sign_up.html'
    form_class = SignUpModelForm
    success_url = '/main/'

    def form_valid(self, form):
        new_user = form.save()
        messages.success(request=self.request,
                         message=f'User {new_user.email} was created')
        login(self.request, new_user, backend=AUTHENTICATION_BACKENDS[0])
        return super(SignUpView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message='Error action')
        return super(SignUpView, self).form_invalid(form)


class LoginView(AuthLoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request,
                         f'Welcome back {form.get_user().email}')
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Error login')
        return super(LoginView, self).form_invalid(form)
