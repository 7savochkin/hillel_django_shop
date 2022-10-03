from django.contrib import admin

from items.models import Item, Category, Product


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('view_item_image', 'name', 'created_at')
    list_filter = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('item',)
