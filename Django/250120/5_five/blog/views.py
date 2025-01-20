from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post


# \site-packages\django\views\generic\list.py
class PostListView(ListView):
    model = Post
    # template_name = "blog/post_list.html"
    # context_object_name = "posts"
    # ordering = ["-created_at"]
    # paginate_by = 10
