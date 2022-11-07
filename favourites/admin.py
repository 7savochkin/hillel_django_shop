from django.contrib import admin

from favourites.models import Favourites


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    filter_horizontal = ('products',)
