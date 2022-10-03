from django.contrib import admin
from django.utils.safestring import mark_safe

from items.models import Item, Category, Product


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('view_item_image', 'name', 'created_at')
    list_filter = ('created_at',)

    def view_item_image(self, obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="64" height="64" />'.format(
                    obj.image.url)))
        return ''


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('view_category_image', 'name')

    def view_category_image(self, obj):
        if obj.image:
            return mark_safe((
                '<img src="{}" width="64" height="64" />'.format(
                    obj.image.url)))
        return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
