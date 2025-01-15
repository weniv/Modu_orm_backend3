from django.urls import path
from .views import blog_list, blog_detail, blog_create, blog_delete

urlpatterns = [
    path("", blog_list, name="blog_list"),
    path("<int:pk>/", blog_detail, name="blog_detail"),
    path("create/<str:title>/", blog_create, name="blog_create"),
    path("delete/<int:pk>/", blog_delete, name="blog_delete"),
]
