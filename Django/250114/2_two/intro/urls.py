from django.urls import path
from .views import greeting, intro, announcement, esg

"""
127.0.0.1:8000/intro/greeting
127.0.0.1:8000/intro/intro
127.0.0.1:8000/intro/announcement
127.0.0.1:8000/intro/esg

# 상세 페이지가 모두 있어야 합니다!
"""

urlpatterns = [
    path("greeting/", greeting),
    path("intro/", intro),
    path("announcement/", announcement),
    path("esg/", esg),
]
