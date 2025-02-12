from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import RedirectView

# 관심사의 분리
# from blog import views


# def root(request):
#     return redirect("/blog/")

# CBV의 as_view 는 : View 함수를 생성하는 생성기
root = RedirectView.as_view(url="/blog/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("", root),
]
