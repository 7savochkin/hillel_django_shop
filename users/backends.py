from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class PhoneModelBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        if phone is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(phone=phone)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and \
                    self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        can = super(PhoneModelBackend, self).user_can_authenticate(user)
        return can and user.is_phone_valid
