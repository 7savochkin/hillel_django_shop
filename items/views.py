from django.shortcuts import render

from items.forms import ItemForm
from items.models import Item


def items(request, *args, **kwargs):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ItemForm()
    context = {
        'items': Item.objects.all(),
        'form': form
    }
    return render(request, 'items/index.html', context=context)
