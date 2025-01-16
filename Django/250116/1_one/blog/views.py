from django.shortcuts import render, redirect
from .models import Post
from django.db.models import Q


def blog_list(request):
    if "q" in request.GET:
        q = request.GET["q"]
        posts = Post.objects.filter(
            Q(title__icontains=q) & Q(content__icontains=q)
        ).distinct()
    else:
        posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"post": post}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request, title, content):
    post = Post.objects.create(title=title, content=content)
    return redirect("blog_detail", pk=post.pk)


def blog_update(request, pk, title, content):
    post = Post.objects.get(pk=pk)
    post.title = title
    post.content = content
    post.save()
    return redirect("blog_detail", pk=post.pk)


def blog_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("blog_list")
