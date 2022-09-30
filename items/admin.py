from django.contrib import admin

from items.models import Item, Category, Product, Discount

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
