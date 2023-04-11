from django.http import HttpResponseNotFound
from django.shortcuts import render

from recipes.models import Recipe


def index(request):
    posts = Recipe.objects.all()
    return render(request, 'recipes/index.html', {'posts': posts})


def about(request):
    return render(request, 'recipes/about.html')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not Found</h1>')
