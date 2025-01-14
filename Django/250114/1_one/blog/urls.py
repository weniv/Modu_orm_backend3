from django.urls import path
from .views import blog_list, blog_details

"""
www.hojun.com/blog           # blog > blog_list (게시물 목록 보는 URL)
www.hojun.com/blog/1         # blog > blog_details (게시물 상세)
www.hojun.com/blog/2         # blog > blog_details (게시물 상세)
www.hojun.com/blog/3         # blog > blog_details (게시물 상세)
"""

urlpatterns = [
    path("", blog_list),
    path("<int:blog_id>/", blog_details),
]
