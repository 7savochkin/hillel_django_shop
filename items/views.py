from django.shortcuts import render


# Create your views here.


def items(request):
    return render(request, 'items.html')


def about(request):
    return render(request, 'about.html')
