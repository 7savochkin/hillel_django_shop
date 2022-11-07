from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_lifecycle import hook, LifecycleModelMixin, AFTER_DELETE, \
    AFTER_SAVE

from shop.mixins.models_mixins import PrimaryKeyMixin


class Feedback(LifecycleModelMixin, PrimaryKeyMixin):
    text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.user.username} | {self.text} | {self.rating}'

    @classmethod
    def _cache_key(cls):
        return 'feedbacks'

    @classmethod
    def get_feedbacks(cls):
        feedbacks = cache.get(cls._cache_key())
        if not feedbacks:
            feedbacks = Feedback.objects.all()
            cache.set(cls._cache_key(), feedbacks)
        return feedbacks

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clear_feedbacks_cache(self):
        cache.delete(self._cache_key())
