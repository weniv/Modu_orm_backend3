from django.urls import path
from django.http import HttpResponse

urlpatterns = [
    path("a/", lambda request: HttpResponse("a")),
    path("b/", lambda request: HttpResponse("b")),
    path("c/", lambda request: HttpResponse("c")),
]
