# from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Post


# # 각 요청을 구별하는 기준 !!! - Router, Dispatcher
# #  URL, 헤더, method, 쿼리스트링 etc
# #  URL을 기준으로 요청을 분기 => 장고의 기본 정책
#
# # 데이터베이스 중심적인 소프트웨어 : 모델, CBV
#
# # 요청을 받으면, View 함수가 호출되어 요청을 처리하고, 반환값을 클라이언트에게 응답
# def index(request: HttpRequest) -> HttpResponse:
#     # ...
#     # text, html, json, image, pdf, video, xls, etc
#     # return HttpResponse("<html><body><h1>Hello World</h1></body></html>")
#     return render(request, template_name="blog/index.html")


# 함수 방식의 단점 : 일부 로직만 변경할 수 없다.
# def make_list_view(qs, paginate_by):
#     def myview(request):
#         # qs = Post.objects.all()  # 조회할 준비 (Lazy)
#         nonlocal qs
#
#         page = int(request.GET.get('page', 1))
#         # paginate_by = 10
#         start_index = (page - 1) * paginate_by
#         end_index = page * paginate_by
#         qs = qs[start_index:end_index]
#
#         # qs = qs.order_by('-pk')  # 일관된 정렬
#         return render(request, "blog/index.html", {
#             "post_list": qs,
#         })
#
#     return myview
#
# index = make_list_view(Post.objects.all(), 10)
# index2 = make_list_view(Article.objects.all(), 20)
# index3 = make_list_view(Menu.objects.all(), 100)

# index = ListView.as_view(
#     model=Post, queryset=Post.objects.all(), paginate_by=10,
#     template_name='blog/index.html',
# )


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()
    paginate_by = 10
    template_name = "blog/index.html"

    # 관심사의 분리
    def get_queryset(self):
        qs = super().get_queryset()

        # less than equal <=
        pk__lte = self.request.GET.get("pk__lte", None)
        if pk__lte is not None:
            qs = qs.filter(pk__lte=pk__lte)

        # ?query=파이썬
        query = self.request.GET.get("query", "").strip()
        if query:
            qs = qs.filter(title__icontains=query)

        return qs


index = PostListView.as_view()


# def index(request):
#     qs = Post.objects.all()  # 조회할 준비 (Lazy)
#
#     page = int(request.GET.get('page', 1))
#     paginate_by = 10
#     start_index = (page -1 ) * paginate_by
#     end_index = page * paginate_by
#     qs = qs[start_index:end_index]
#
#     # qs = qs.order_by('-pk')  # 일관된 정렬
#     return render(request, "blog/index.html", {
#         "post_list": qs,
#     })
