from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from main.views import index, a, b, c


# def index(request):
#     return HttpResponse("Hello, world.")


# def a(request):
#     return HttpResponse("Hello, world a!")


# def b(request):
#     return HttpResponse("Hello, world b!")


# def c(request):
#     return HttpResponse("Hello, world c?")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("a/", a),
    path("b/", b),
    path("c", c),
    # '/'가 있든 없든 동일하게 처리를 해줍니다. 다만, 구버전에서는 '/'가 없으면 그 뒤에 나오는 문자열도 같이 처리해줍니다.
]
