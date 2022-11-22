from django.contrib import admin
from django.contrib.admin import register

from tracking.models import Tracking


@register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    readonly_fields = ('method', 'url', 'data')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
