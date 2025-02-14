from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView

from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer

# content : 4KB
# def post_list(request):
#     qs = Post.objects.all().defer("content").select_related("author")
#     serializer = PostListSerializer(qs, many=True)
#     return JsonResponse(serializer.data, safe=False)

post_list = ListAPIView.as_view(
    queryset=PostListSerializer.get_optimized_queryset(),
    serializer_class=PostListSerializer,
)

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     serializer = PostDetailSerializer(post)
#     return JsonResponse(serializer.data)


post_detail = RetrieveAPIView.as_view(
    queryset=PostDetailSerializer.get_optimized_queryset(),
    serializer_class=PostDetailSerializer,
)
