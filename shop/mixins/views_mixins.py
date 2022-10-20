from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View


class StaffUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
