from django.urls import path, include
from .views import MyView

urlpatterns = [
    path("myview/", MyView.as_view()),
    path("blog/", include("blog.urls")),
]
