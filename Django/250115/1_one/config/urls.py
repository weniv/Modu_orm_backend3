from django.contrib import admin
from django.urls import path, include, re_path
from blog.views import blog_list, blog_detail
from django.http import HttpResponse

"""
path(route, view, kwargs=None, name=None)
"""


def year_archive(request, year, mon, day):
    print(year)
    print(mon)
    print(day)
    return HttpResponse(f"{year}년에 대한 내용입니다.")


def reg_a(request, num, s):
    print(num)
    print(s)
    return HttpResponse(f"{num}, {s}")


def reg_b(request, a, b, c):
    print(a, b, c)
    return HttpResponse(f"{a}, {b}, {c}")


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("config.urlstest")),
    # 이렇게 .py파일을 여러개로 나누어서 URL을 분기하여 관리할 수 있습니다. URL이 수십개 되는 경우 이렇게 관리하세요. 다만, URL이 하나의 앱에 수십개라면 처음부터 설계가 잘못되었는지 체크를 해볼필요가 있습니다.
    # path("urls/", include("hello.urlstest")),
    # path("blog/", blog_list, name="blog_list"),
    # path("blog/<int:value>/", blog_detail, {"hello": "world"}, name="blog_detail"),
    re_path(r"^reg/(?P<year>[0-9]{4})/$", year_archive),
    re_path(r"^reg/(?P<year>[0-9]{4})_(?P<mon>[0-9]{2})_(?P<day>[0-9]{2})/$", reg_a),
    re_path(r"^reg/(?P<a>[a-zA-Z]+)/(?P<b>[a-zA-Z]+)/(?P<c>[a-zA-Z]+)/$", reg_b),
]
