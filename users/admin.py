from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    permissions_fieldsets = {
        'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups',
                   'user_permissions'),
        'classes': ('collapse',),
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'phone', 'is_phone_valid')}),
        (_('Info'),
         {'fields': ('last_login', 'date_joined',)}),
    )
    list_display = (
        'id', 'email', 'phone', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)
