from django.shortcuts import render

from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback


def feedbacks(request, *args, **kwargs):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FeedbackForm()
    context = {
        'feedbacks': Feedback.objects.all(),
        'form': form,
    }
    return render(request, 'feedbacks/index.html', context=context)
