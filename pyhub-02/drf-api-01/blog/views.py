# blog/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import PostForm, TagForm
from .models import Post, Tag
from .generics import View, APIView


def whoami(request):
    status = 200 if request.user.is_authenticated else 401
    username = request.user.username or "anonymous"
    return HttpResponse(f"Your username is <strong>{username}</strong>.", status=status)


class PostListView(APIView):
    model = Post  # 클래스 변수를 설정

    def get_queryset(self):
        # # 부모의 쿼리셋을 이어받아서 수행
        # qs = super().get_queryset()
        # # qs = qs.filter(...)
        # return qs

        # 자식이 직접 쿼리셋을 생성
        return Post.objects.all()


post_list = PostListView.as_view()

# post_list = View.as_view(model=Post)

# def post_list(request: HttpRequest) -> HttpResponse:
#     post_qs = Post.objects.all()
#     return render(request=request, template_name="blog/post_list.html", context={
#         "post_list": post_qs,
#     })


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    return render(
        request=request,
        template_name="blog/post_detail.html",
        context={
            "post": post,
        },
    )


@login_required
def post_new(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = PostForm()
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            created_post = form.save(commit=False)
            created_post.author = request.user
            created_post.save()
            return redirect(to="blog:post_detail", pk=created_post.pk)

    return render(
        request=request,
        template_name="blog/post_form.html",
        context={
            "form": form,
        },
    )


@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        form = PostForm(instance=post)
    else:
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            created_post = form.save()
            return redirect(to="blog:post_detail", pk=created_post.pk)

    return render(
        request=request,
        template_name="blog/post_form.html",
        context={
            "form": form,
            "post": post,
        },
    )


@login_required
def post_delete(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect(to="blog:post_list")

    return render(
        request=request,
        template_name="blog/post_confirm_delete.html",
        context={
            "post": post,
        },
    )


# def tag_list(request):
#     tag_qs = Tag.objects.all()
#
#     query = request.GET.get("query", "")
#     if query:
#         tag_qs = tag_qs.filter(name__icontains=query)
#
#     # is_htmx: bool = request.META.get("HTTP_HX_REQUEST") == "true"
#     if request.htmx:
#         # if "partial" in request.GET:
#         template_name = "blog/_tag_list.html"  # 레이아웃 없이 컨텐츠 만 !
#     else:
#         template_name = "blog/tag_list.html"  # 레이아웃 포함, 컨텐츠 없음.
#
#     return render(
#         request,
#         template_name,
#         {
#             "tag_list": tag_qs,
#         },
#     )


class TagListView(ListView):
    model = Tag
    queryset = Tag.objects.all()
    # template_name = "blog/tag_list.html"  # 고정
    paginate_by = 10  # ADDED

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.GET.get("query", "")
        if query:
            qs = qs.filter(name__icontains=query)

        return qs

    def get_template_names(self):
        if self.request.htmx:
            return ["blog/_tag_list.html"]
        return super().get_template_names()


tag_list = TagListView.as_view()


def tag_new(request):
    if request.method == "GET":
        form = TagForm()
    else:
        form = TagForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "태그를 저장했습니다.")
            return redirect("blog:tag_list")

    template_name = "blog/tag_form.html"

    return render(
        request,
        template_name,
        {
            "form": form,
        },
    )
