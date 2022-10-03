from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'In money'
    PERCENT = 1, 'In percent'
