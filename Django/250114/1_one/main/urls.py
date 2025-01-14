from django.urls import path
from .views import index

"""
www.hojun.com/
"""

urlpatterns = [
    path("", index),
]
