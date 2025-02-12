from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# 각 요청을 구별하는 기준 !!! - Router, Dispatcher
#  URL, 헤더, method, 쿼리스트링 etc
#  URL을 기준으로 요청을 분기 => 장고의 기본 정책


# 요청을 받으면, View 함수가 호출되어 요청을 처리하고, 반환값을 클라이언트에게 응답
def index(request: HttpRequest) -> HttpResponse:
    # ...
    # text, html, json, image, pdf, video, xls, etc
    return HttpResponse("<html><body><h1>Hello World</h1></body></html>")
