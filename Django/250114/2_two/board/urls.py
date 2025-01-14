from django.urls import path
from .views import (
    notice,
    notice_detail,
    recruitment,
    recruitment_detail,
    other,
    other_detail,
)

"""
127.0.0.1:8000/board/notice
# 127.0.0.1:8000/board/notice/1
127.0.0.1:8000/board/recruitment
127.0.0.1:8000/board/other
"""

urlpatterns = [
    path("notice/", notice),
    path("notice/<int:pk>", notice_detail),
    path("recruitment/", recruitment),
    path("recruitment/<int:pk>", recruitment_detail),
    path("other/", other),
    path("other/<int:pk>", other_detail),
]
