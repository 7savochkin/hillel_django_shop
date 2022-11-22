import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from feedbacks.model_forms import FeedbackModelForm
from feedbacks.models import Feedback


@login_required
def feedbacks(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        form = FeedbackModelForm(user=user, data=request.POST)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.text = re.sub(r'(\<(/?[^>]+)>)', '',
                                       f'{form.cleaned_data.get("text")}')
            messages.success(request,
                             message=f'Thank {new_feedback.user.email} for feedbacks!')  # noqa
            new_feedback.save()
        else:
            messages.error(request,
                           message='Ensure this value is less than or equal to 5.') # noqa
    else:
        form = FeedbackModelForm(user=user)
    context = {
        'feedbacks': Feedback.get_feedbacks(),
        'form': form,
    }
    return render(request, 'feedbacks/index.html', context=context)
