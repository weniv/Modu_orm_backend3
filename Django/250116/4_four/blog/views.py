# blog > views.py
from django.shortcuts import render
from django.db.models import Q
from .models import Post
from django.shortcuts import redirect
from .forms import PostForm

# from .forms import PostForm


def blog_list(request):
    if request.GET.get("q"):
        db = Post.objects.filter(
            Q(title__contains=request.GET.get("q"))
            | Q(contents__contains=request.GET.get("q"))
        ).distinct()
    else:
        db = Post.objects.all()
    context = {"object_list": db}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"object": post}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    form = PostForm()
    context = {"form": form}
    return render(request, "blog/blog_create.html", context)
