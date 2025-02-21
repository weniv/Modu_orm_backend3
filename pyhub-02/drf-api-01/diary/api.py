from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    GenericAPIView,
)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
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


class MapModelViewSet(ModelViewSet):
    permission_classes_map = {}
    serializer_class_map = {}
    queryset_map = {}

    def get_permissions(self):
        try:
            classes = self.permission_classes_map[self.action]
            return [cls() for cls in classes]
        except KeyError:
            return super().get_permissions()

    def get_serializer_class(self):
        # self.request.method  # "GET"
        # self.action  # "list", "retrieve", "create", "update", "partial_update", "destroy"
        try:
            return self.serializer_class_map[self.action]
        except KeyError:
            return super().get_serializer_class()

    def get_queryset(self):
        try:
            # queryset_map 에 정의된 쿼리셋이 있다면 활용합니다.
            return self.queryset_map[self.action]
        except KeyError:
            # queryset_map에 정의된 쿼리셋이 없고, 시리얼라이저 클래스에 get_optimized_queryset 속성이 있다면
            # 이를 호출하여 쿼리셋을 반환합니다.
            serializer_class = self.get_serializer_class()
            if hasattr(serializer_class, "get_optimized_queryset"):
                return serializer_class.get_optimized_queryset()

            # 클래스 변수에 지정된 쿼리셋을 반환합니다.
            return super().get_queryset()


# 기본 5개의 API Endpoint 생성 + 물론 추가 Endpoint 도 가능 !!!
class PostViewSet(MapModelViewSet):
    queryset = Post.objects.exclude(status=Post.Status.DELETED)
    serializer_class = PostSerializer

    permission_classes_map = {
        "list": [AllowAny],
    }
    serializer_class_map = {
        "list": PostListSerializer,
    }
    queryset_map = {
        # "list": PostListSerializer.get_optimized_queryset(),
        # "retrieve": Post.objects.exclude(status=Post.Status.DELETED),
        # "update": Post.objects.exclude(status=Post.Status.DELETED),
        # "partial_update": Post.objects.exclude(status=Post.Status.DELETED),
        # "destroy": Post.objects.exclude(status=Post.Status.DELETED),
    }

    # permission_classes = [AllowAny]  # 5개 API에 모두 적용

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete()


# class PostListAPIView(ListAPIView):
#     queryset = PostListSerializer.get_optimized_queryset()
#     serializer_class = PostListSerializer
#     permission_classes = [AllowAny]

# post_list = PostListAPIView.as_view()


# class PostCreateAPIView(CreateAPIView):
#     serializer_class = PostSerializer
#     # API 별로 권한 설정
#     # permission_classes = [
#     #     # AllowAny,
#     #     IsAuthenticated,
#     # ]
#
#     def perform_create(self, serializer):
#         # commit인자는 ModelForm만 지원할 뿐
#         # ModelSeralizer에서는 지원하지 않아요.
#         # serializer.save(commit=False)  # XXX
#
#         serializer.save(
#             user=self.request.user,
#             # ip=...,
#         )

# post_new = PostCreateAPIView.as_view()

# @api_view(["PUT"])
# def post_edit(request: Request, pk) -> Response:
#     post = get_object_or_404(Post, pk=pk)
#
#     serializer = PostSerializer(data=request.data, instance=post)
#     if serializer.is_valid():
#         post = serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)


# class PostUpdateAPIView(UpdateAPIView):
#     queryset = Post.objects.exclude(status=Post.Status.DELETED)  # 범위
#     serializer_class = PostSerializer
#
#
# post_edit = PostUpdateAPIView.as_view()
#
#
# class PostDestroyAPIView(DestroyAPIView):
#     queryset = Post.objects.exclude(status=Post.Status.DELETED)  # 범위
#
#     # Soft Delete
#     def perform_destroy(self, instance: Post):
#         # instance.content = ""
#         # instance.status = Post.Status.DELETED
#         # instance.save()  # 모든 필드 값을 데이터베이스에 UPDATE 시도
#         instance.soft_delete()
#
#
# post_delete = PostDestroyAPIView.as_view()


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


# class PostListCreateAPIView(CreateModelMixin, ListModelMixin, GenericAPIView):
#
#     # list
#     queryset = PostListSerializer.get_optimized_queryset()
#     # serializer_class = PostListSerializer
#     permission_classes = [AllowAny]
#
#     # create
#     # serializer_class = PostSerializer
#
#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return PostListSerializer
#         return PostSerializer
#
#     def perform_create(self, serializer):
#         # commit인자는 ModelForm만 지원할 뿐
#         # ModelSeralizer에서는 지원하지 않아요.
#         # serializer.save(commit=False)  # XXX
#
#         serializer.save(
#             user=self.request.user,
#             # ip=...,
#         )
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
