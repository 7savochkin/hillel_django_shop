from django.shortcuts import render

from feedbacks.forms import FeedbackForm


def feedbacks(request, *args, **kwargs):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FeedbackForm()
    context = {
        'form': form,
    }
    return render(request, 'feedbacks/index.html', context=context)
