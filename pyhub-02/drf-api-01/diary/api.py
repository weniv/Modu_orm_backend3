from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from diary.models import Comment
from diary.serializers import PostSerializer, CommentSerializer


@api_view(["POST"])
def post_new(request: Request) -> Response:
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


def comment_list(request, post_pk):
    qs = Comment.objects.all()
    qs = qs.filter(post__pk=post_pk)

    # 커스텀이 어려운 쿼리셋 만을 통한 파이썬 기본 데이터 타입 변환
    # list(qs.values())

    # QuerySet -> Python 기본 데이터 타입 by Serializer
    serializer = CommentSerializer(
        instance=qs,  # QuerySet or Model Instance
        many=True,  # QuerySet인 경우 True
    )
    return JsonResponse(serializer.data, safe=False)
