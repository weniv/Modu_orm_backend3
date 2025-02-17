from django.shortcuts import render
from django.views.generic import ListView, DetailView

from diary.models import Post, Comment


# as_view 함수는 언제 호출되는가 ??
# post_list = ListView.as_view(model=Post)


class PostListView(ListView):
    model = Post
    # template_name = "..."

post_list = PostListView.as_view()


post_detail = DetailView.as_view(model=Post)
# context_data로서 comment_list 쿼리셋을 추가


class CommentListView(ListView):
    model = Comment

    def get_queryset(self):
        post_pk = self.kwargs["post_pk"]
        qs = super().get_queryset()
        qs = qs.filter(post__pk=post_pk)
        return qs


comment_list = CommentListView.as_view()
