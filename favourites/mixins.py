from favourites.models import Favourites


class GetFavouritesMixin:

    def get_favourites_object(self):
        return Favourites.objects.get_or_create(
            user=self.request.user
        )[0]
