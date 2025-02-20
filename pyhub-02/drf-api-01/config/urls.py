from django.contrib import admin
from django.apps import apps
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("chat/", include("chat.urls")),
    path("melon/", include("melon.urls")),
    path("health/", include("health.urls")),
    path("diary/", include("diary.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

if apps.is_installed("debug_toolbar"):
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
