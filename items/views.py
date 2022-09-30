from django.shortcuts import render


def items(request, *args, **kwargs):
    return render(request, 'items/index.html')
