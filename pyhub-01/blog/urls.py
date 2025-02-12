from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    # path("new/", views.post_new),
    # path("<pk:int>/", views.post_detail),
    # path("<pk:int>/edit/", views.post_edit),
    # path("<pk:int>/delete/", views.post_delete),
]
