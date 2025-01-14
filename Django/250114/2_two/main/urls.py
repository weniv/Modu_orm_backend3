from django.urls import path
from django.http import HttpResponse

"""
127.0.0.1:8000/
"""


def index(request):
    return HttpResponse("index")


urlpatterns = [
    path("", index),
]
