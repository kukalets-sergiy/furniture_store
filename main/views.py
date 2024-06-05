from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):


    context = {
        'title': 'Home - Main',
        'content': "",
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Home - About',
        'content': "About",
        'text_on_page': "Good store"
    }

    return render(request, 'main/about.html', context)
