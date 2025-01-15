from django.shortcuts import render
from django.http import HttpResponse


def blog_list(request):
    # return HttpResponse("blog_list")
    return render(request, "blog/blog_list.html")


def blog_detail(request, value, hello):
    # blog_detail(request, value, **hello) # object 전체로 받습니다.
    # blog_detail(request, value, hello) # key로 hello를 가져옵니다.
    # return HttpResponse(f"blog_detail {value}, {hello}")
    print(value, hello)
    return render(request, "blog/blog_detail.html")
