from favourites.models import Favourites


class GetFavouritesMixin:

    def get_favourites_object(self):
        return Favourites.objects.select_related('user').prefetch_related(
            'products').get_or_create(user=self.request.user)[0]
