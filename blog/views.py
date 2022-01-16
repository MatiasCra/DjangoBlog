from django.shortcuts import render
from .forms import PostForm


def index(request):
    return render(request, 'blog/index.html')


def categories(request):
    return render(request, 'blog/categories.html')


def myposts(request):
    return render(request, 'blog/myposts.html')


def create(request):
    form = PostForm()
    return render(request, "blog/create.html", {"form": form})