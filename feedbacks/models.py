from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shop.mixins.models_mixins import PrimaryKeyMixin


class Feedback(PrimaryKeyMixin):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        if feedbacks:
            cache.delete(cls._cache_key())
        cache.set(cls._cache_key(), Feedback.objects.all())
        return cache.get(cls._cache_key())
