from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostList(ListView):
    model = Post
    ordering = "-pk"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "")
        if q:
            queryset = queryset.filter(Q(title__contains=q) | Q(content__contains=q))
        return queryset


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    login_url = "/accounts/login/"


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "head_image", "file_upload"]
    success_url = reverse_lazy("blog_list")
    login_url = "/accounts/login/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = "__all__"
    success_url = reverse_lazy("blog_list")
    login_url = "/accounts/login/"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog_list")
    login_url = "/accounts/login/"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostTest(CreateView):
    model = Post

    def get(self, request):
        return HttpResponse("GET 요청을 잘 받았습니다.")

    def post(self, request):
        return HttpResponse("POST 요청을 잘 받았습니다.")


blog_list = PostList.as_view()
blog_detail = PostDetail.as_view()
blog_write = PostCreate.as_view()
blog_edit = PostUpdate.as_view()
blog_delete = PostDelete.as_view()
test = PostTest.as_view()
