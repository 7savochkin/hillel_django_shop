from django.contrib import admin

from items.models import Item, Category, Product


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ...
