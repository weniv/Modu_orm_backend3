from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import api
from .api import PostViewSet

app_name = "diary"  # URL Reverse 에서의 namespace

urlpatterns = [
    path("", views.post_list, name="post-list"),
    path("<int:pk>/", views.post_detail, name="post-detail"),
    path("new/", views.post_new, name="post-new"),
    path("<int:pk>/edit/", views.post_edit, name="post-edit"),
    path("<int:post_pk>/comments/", views.comment_list, name="comment-list"),
    path("<int:post_pk>/comments/new/", views.comment_new, name="comment-new"),
]

router = DefaultRouter()
router.register("posts", PostViewSet)
urlpatterns_api_v1 = router.urls

# urlpatterns_api_v1 = [
#     path("posts/", api.post_list, name="post-list"),
#     path("posts/new/", api.post_new, name="post-new"),
#     path("posts/<int:pk>/edit/", api.post_edit, name="post-edit"),
#     path("posts/<int:pk>/delete/", api.post_delete, name="post-delete"),
#     path("posts/<int:post_pk>/comments/", api.comment_list, name="comment-list"),
# ]

urlpatterns += [
    path("api/v1/", include((urlpatterns_api_v1, "api-v1"))),
]
