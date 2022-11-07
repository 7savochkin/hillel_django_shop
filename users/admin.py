from django.contrib import admin # noqa

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...
