from django.http import JsonResponse

from diary.models import Comment
from diary.serializers import CommentSerializer


def comment_list(request, post_pk):
    qs = Comment.objects.all()
    qs = qs.filter(post__pk=post_pk)

    # 커스텀이 어려운 쿼리셋 만을 통한 파이썬 기본 데이터 타입 변환
    # list(qs.values())

    # QuerySet -> Python 기본 데이터 타입 by Serializer
    serializer = CommentSerializer(
        qs,  # QuerySet or Model Instance
        many=True,  # QuerySet인 경우 True
    )
    return JsonResponse(serializer.data, safe=False)
