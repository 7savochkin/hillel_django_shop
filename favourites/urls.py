from django.urls import path

from favourites.views import FavouritesView, DeleteFavouritesView, \
    AddOrDeleteFavouritesView, AJAXAddOrDeleteFavouritesView

urlpatterns = [
    path('favourites/', FavouritesView.as_view(), name='favourites'),
    path('add-or-delete-to-favourites/<uuid:pk>', AddOrDeleteFavouritesView.as_view(), name='add_favourites'), # noqa
    path('ajax-add-or-delete-to-favourites/<uuid:pk>', AJAXAddOrDeleteFavouritesView.as_view(), name='ajax_add_favourites'), # noqa
    path('del_from/', DeleteFavouritesView.as_view(), name='delete_favourites'), # noqa
]
