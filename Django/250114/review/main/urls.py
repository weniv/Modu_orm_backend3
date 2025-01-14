from django.urls import path
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, Django!")


urlpatterns = [
    path("", index),
]
