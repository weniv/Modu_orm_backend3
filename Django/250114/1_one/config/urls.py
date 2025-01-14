from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # main, blog, accounts 앱의 urls.py를 include 한다.
    path("", include("main.urls")),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
]
