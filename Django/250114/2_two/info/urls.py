from django.urls import path
from .views import pressrelease, prgallary, archives

"""
127.0.0.1:8000/info/pressrelease
127.0.0.1:8000/info/prgallary
127.0.0.1:8000/info/archives
# 다 상세 페이지가 있어야 합니다. 생략된 형태입니다.
"""

urlpatterns = [
    path("pressrelease/", pressrelease),
    path("prgallary/", prgallary),
    path("archives/", archives),
]
