from django.urls import path

from melon.views import song_list

urlpatterns = [
    path("", song_list),
]
