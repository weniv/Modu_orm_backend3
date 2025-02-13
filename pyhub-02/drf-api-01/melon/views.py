# melon/views.py

from django.db.models import F
from django.db.models.functions import Length
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from melon.models import Song

from .serializers import SongSerializer

# /melon/?format=json    Query String
# def song_list(request: HttpRequest) -> HttpResponse:
#     song_qs = Song.objects.annotate(title_length=Length(F("title")))

#     # QueryDict 타입 <- QueryString을 사전 타입으로 제공
#     fmt = request.GET.get("format", "html")
#     if fmt == "json":
#         # 1) JSON 포맷의 직렬화
#         song_list_data = list(song_qs.values("title", "title_length"))
#         # 내부에서 json.dumps를 활용하여 객체 -> str
#         return JsonResponse(song_list_data, safe=False)
#     else:
#         # 2) HTML 포맷의 직렬화
#         return render(
#             request,
#             "melon/song_list.html",
#             {
#                 "song_list": song_qs,
#             },
#         )


# def song_list(request: HttpRequest) -> HttpResponse:
#     song_qs = Song.objects.annotate(title_length=Length(F("title")))

#     # song_list_data = list(song_qs.values("title", "title_length"))

#     # 관심사의 분리 : 직렬화 로직을 뷰 함수에서 분리
#     serializer = SongSerializer(instance=song_qs, many=True)
#     # 정확히는 list를 상속받은 ReturnList 타입
#     song_list_data = serializer.data  # list

#     return JsonResponse(song_list_data, safe=False)


# 장고 View => 함수 기반
# DRF APIView => 클래스 기반


# @api_view(["GET"])  # 장식자를 통해서 클래스로 변환
# def song_list(request: Request) -> Response:
#     song_qs = Song.objects.annotate(title_length=Length(F("title")))

#     # song_list_data = list(song_qs.values("title", "title_length"))

#     # 관심사의 분리 : 직렬화 로직을 뷰 함수에서 분리
#     serializer = SongSerializer(instance=song_qs, many=True)
#     # 정확히는 list를 상속받은 ReturnList 타입
#     song_list_data = serializer.data  # list

#     return Response(song_list_data)


# class SongListAPView(ListAPIView):
#     queryset = Song.objects.annotate(title_length=Length(F("title")))
#     serializer_class = SongSerializer


# song_list = SongListAPView.as_view()


class SongViewSet(ModelViewSet):
    queryset = Song.objects.annotate(title_length=Length(F("title")))
    serializer_class = SongSerializer
    # list 메서드, retrieve 메서드, create, update, destroy 메서드가 이미 구현


# 매핑 !!!
song_list = SongViewSet.as_view({"get": "list"})
