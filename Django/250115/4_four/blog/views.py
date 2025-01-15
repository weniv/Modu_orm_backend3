from django.shortcuts import render
from .models import Post


def blog_list(request):
    blogs = Post.objects.all()
    context = {"object_list": blogs}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    blog = Post.objects.get(pk=pk)
    context = {"object": blog}
    return render(request, "blog/blog_detail.html", context)
