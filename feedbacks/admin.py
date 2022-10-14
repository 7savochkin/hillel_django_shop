from django.contrib import admin

from feedbacks.models import Feedback


@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    ...
