from django.contrib import admin

from currencies.models import CurrencyHistory


@admin.register(CurrencyHistory)
class CurrencyHistory(admin.ModelAdmin):
    readonly_fields = ('currency', 'buy', 'sale', 'created_at')
    list_display = ('currency', 'created_at', 'buy', 'sale')
