from django.urls import path, include
from . import api
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("new/", views.post_new, name="post_new"),
    path("<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
]

urlpatterns_api_v1 = [
    path("", api.post_list, name="post_list"),
    path("<int:pk>/", api.post_detail, name="post_detail"),
    # path("new/", api.post_new, name="post_new"),
    # path("<int:pk>/edit/", api.post_edit, name="post_edit"),
    # path("<int:pk>/delete/", api.post_delete, name="post_delete"),
]

urlpatterns += [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
]