from django.contrib import admin

from config.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    ...
