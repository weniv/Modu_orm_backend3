from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("write/", views.blog_write, name="blog_write"),
    path("edit/<int:pk>/", views.blog_edit, name="blog_edit"),
    path("delete/<int:pk>/", views.blog_delete, name="blog_delete"),
    path("test/", views.test, name="test"),
]
