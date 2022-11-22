from django.db import models

from shop.mixins.models_mixins import PrimaryKeyMixin


class Tracking(PrimaryKeyMixin):
    method = models.CharField(max_length=16)
    url = models.CharField(max_length=255)
    data = models.JSONField(default=dict)
