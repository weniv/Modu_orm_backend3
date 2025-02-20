from django.urls import path, include
from django.views.generic import TemplateView

from . import api
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("new/", views.post_new, name="post_new"),
    path("<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("tags/", views.tag_list, name="tag_list"),
    path("tags/new/", views.tag_new, name="tag_new"),
    path("tags/<int:pk>/delete/", views.tag_delete, name="tag_delete"),
]

urlpatterns += [
    path("test/", TemplateView.as_view(template_name="blog/test.html"), name="index"),
    path("whoami/", views.whoami, name="whoami"),
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
