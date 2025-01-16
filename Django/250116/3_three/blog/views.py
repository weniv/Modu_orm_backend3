from django.shortcuts import render
from .models import Post


def index(request):
    print(request)
    print(request.GET)
    print(request.POST)
    posts = Post.objects.all()
    return render(request, "blog/index.html", {"posts": posts})
