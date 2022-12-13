from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, RedirectView
from django.contrib.auth.views import LoginView as AuthLoginView

from users.forms import SignUpModelForm, CustomAuthenticationForm, \
    SignUpPhoneConfirmForm

User = get_user_model()


class SignUpView(FormView):
    form_class = SignUpModelForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('sign_up_phone_confirm')

    def form_valid(self, form):
        user = form.save()
        self.request.session['user_id'] = user.id
        return super().form_valid(form)


class SignUpEmailConfirm(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs['uidb64'])

        if user is not None:
            token = kwargs['token']
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save(update_fields=('is_active',))
                messages.success(
                    request,
                    'Activation success. '
                    'You can login using your email and password.'
                )
            else:
                messages.error(request, 'Activation error.')
        return super().get(request, *args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist,
                ValidationError):
            user = None
        return user


class SignUpPhoneConfirm(FormView):
    form_class = SignUpPhoneConfirmForm
    template_name = 'registration/sign_up_phone_confirm.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid(session_user_id=request.session['user_id']):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save(self.request.session['user_id'])
        messages.success(self.request, message='Your account was activated,'
                                               ' you can sign in!')
        return super(SignUpPhoneConfirm, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message='Please, write valid code!')
        return super(SignUpPhoneConfirm, self).form_invalid(form)


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
