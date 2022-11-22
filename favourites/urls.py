from django.urls import path

from favourites.views import FavouritesView, DeleteFavouritesView, \
    AddFavouritesView

urlpatterns = [
    path('favourites/', FavouritesView.as_view(), name='favourites'),
    path('add_to/', AddFavouritesView.as_view(), name='add_favourites'),
    path('del_from/', DeleteFavouritesView.as_view(), name='delete_favourites'), # noqa
]
