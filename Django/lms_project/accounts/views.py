from django.shortcuts import render

# Create your views here.

from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # 도서 관련
    path('', views.book_list, name='book-list'),
    path('<int:pk>/', views.book_detail, name='book-detail'),
    path('create/', views.book_create, name='book-create'),
    path('<int:pk>/update/', views.book_update, name='book-update'),
    path('<int:pk>/delete/', views.book_delete, name='book-delete'),
]