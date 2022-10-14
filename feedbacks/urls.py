from feedbacks.views import feedbacks
from django.urls import path

urlpatterns = [
    path('feedbacks/', feedbacks, name='feedbacks'),
]
