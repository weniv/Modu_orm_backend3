from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("board/", include("board.urls")),
    path("info/", include("info.urls")),
    path("intro/", include("intro.urls")),
]
