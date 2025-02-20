from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from diary.models import Post, Comment
from diary.serializers import PostSerializer, CommentSerializer, PostListSerializer


# @api_view(["POST"])
# def post_new(request: Request) -> Response:
#     serializer = PostSerializer(data=request.data)
#     if serializer.is_valid():
#         post = serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.exclude(status=Post.Status.DELETED)  # 범위
    serializer_class = PostSerializer

    permission_classes_map = {
        "list": [AllowAny],
        "retrieve": [AllowAny],
    }
    serializer_class_map = {
        "list": PostListSerializer,
    }

    def get_permissions(self):
        try:
            classes = self.permission_classes_map[self.action]
            return [cls() for cls in classes]
        except KeyError:
            return super().get_permissions()

    def get_serializer_class(self):
        try:
            return self.serializer_class_map[self.action]
        except KeyError:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance: Post):
        # instance.content = ""
        # instance.status = Post.Status.DELETED
        # instance.save()  # 모든 필드 값을 데이터베이스에 UPDATE 시도
        instance.soft_delete()


# def comment_list(request, post_pk):
#     qs = Comment.objects.all()
#     qs = qs.filter(post__pk=post_pk)
#
#     # 커스텀이 어려운 쿼리셋 만을 통한 파이썬 기본 데이터 타입 변환
#     # list(qs.values())
#
#     # QuerySet -> Python 기본 데이터 타입 by Serializer
#     serializer = CommentSerializer(
#         instance=qs,  # QuerySet or Model Instance
#         many=True,  # QuerySet인 경우 True
#     )
#     return JsonResponse(serializer.data, safe=False)


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs["post_pk"]
        qs = super().get_queryset()
        qs = qs.filter(post__pk=post_pk)
        return qs


comment_list = CommentListAPIView.as_view()
