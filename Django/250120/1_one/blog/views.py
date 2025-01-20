from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post
from .forms import PostForm


def blog_list(request):
    if request.GET.get("q"):
        posts = Post.objects.filter(
            Q(title__contains=request.GET.get("q"))
            | Q(content__contains=request.GET.get("q"))
        ).distinct()
        context = {"posts": posts}
        return render(request, "blog/blog_list.html", context)
    posts = Post.objects.all()
    return render(request, "blog/blog_list.html")


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"post": post}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            # app_name이 있을 경우
            # 이렇게 설정하면 많은 앱이 있었을 때 유리합니다.
            # return redirect("blog:blog_list")
            return redirect("blog_list")
        else:
            context = {
                "form": form,
                "error": "입력이 올바르지 않습니다!!!!!!! 다시 작성!!",
            }
            return render(request, "blog/blog_create.html", context)


def blog_update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "GET":
        form = PostForm(instance=post)
        context = {"form": form}
        # blog_create.html을 재사용해도 됨
        return render(request, "blog/blog_update.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)
        else:
            context = {
                "form": form,
                "error": "입력이 올바르지 않습니다!!!!!!! 다시 작성!!",
            }
            return render(request, "blog/blog_update.html", context)


def blog_delete(request, pk):
    # 못찾을 경우 error
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
    return redirect("blog_list")
