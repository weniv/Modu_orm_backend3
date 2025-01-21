from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("settings/", lambda request: HttpResponse(settings.NAME)),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
