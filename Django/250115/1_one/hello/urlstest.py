from django.urls import path
from django.http import HttpResponse

urlpatterns = [
    path("aa/", lambda request: HttpResponse("aa")),
    path("bb/", lambda request: HttpResponse("bb")),
    path("cc/", lambda request: HttpResponse("cc")),
]
