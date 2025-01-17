from django.shortcuts import render, redirect
from .models import Post
from .forms import PostFrom
from django.contrib.auth.models import User


def blog_list(request):
    """
    (V)get, (V)q(querystring)
    """
    if request.GET.get("q"):
        q = request.GET["q"]
        posts = Post.objects.filter(title__contains=q)
    else:
        posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    """
    (V)get
    """
    post = Post.objects.get(pk=pk)
    context = {"post": post}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    """
    (V)post
    """
    if request.method == "POST":
        form = PostFrom(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # 임시저장
            post.author = User.objects.first()  # 임시로 첫번째 유저를 author로 지정
            post.save()
            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostFrom()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)


def blog_update(request, pk):
    """
    (V)post
    """
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        post = Post.objects.get(pk=pk)
        post.title = title
        post.content = content
        post.save()
        return redirect("blog_detail", pk=post.pk)
    else:
        post = Post.objects.get(pk=pk)
        form = PostFrom(instance=post)
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)


def blog_delete(request, pk):
    """
    (V)post지만 일단 get처리
    """
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect("blog_list")
