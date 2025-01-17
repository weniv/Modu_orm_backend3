from django.urls import path
from .views import blog_list, blog_detail, blog_create, blog_update, blog_delete

urlpatterns = [
    # get, q(querystring)
    path("", blog_list, name="blog_list"),
    # get
    path("<int:pk>/", blog_detail, name="blog_detail"),
    # login, post
    path("create/", blog_create, name="blog_create"),
    # login(auth==login), post
    path("update/<int:pk>/", blog_update, name="blog_update"),
    # login(auth==login), post
    path("delete/<int:pk>/", blog_delete, name="blog_delete"),
]
