from django.shortcuts import render, redirect
from .models import Post
from django.shortcuts import get_object_or_404


def blog_list(request):
    blogs = Post.objects.all()
    context = {"object_list": blogs}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, pk):
    blog = Post.objects.get(pk=pk)
    context = {"object": blog}
    return render(request, "blog/blog_detail.html", context)


def blog_create(request, title):
    content = f"hello world {title}"
    Post.objects.create(title=title, content=content)
    return redirect("blog_list")


def blog_delete(request, pk):
    # q = Post.objects.get(pk=pk)
    # q.delete()
    # 이 코드는 만약 pk가 없으면 에러가 발생됩니다.
    # 만약 못찾는 경우를 대비하기 위해서
    # Post.objects.get(pk=pk).delete()
    # 위 코드를 사용할 수도 있습니다.
    # 다만 보다 확실하게 404 페이지로 넘겨줄 수 있도록 아래와 같은 코드를 사용하시길 권해드립니다.
    q = get_object_or_404(Post, pk=pk)
    # 여기서 만약 못찾는 경우 404 페이지를 보여줍니다.
    q.delete()
    return redirect("blog_list")
