from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse

"""
이 예제가 시사하는 바
1. render 함수로 읽어온 .html 파일은 사실 문자열입니다.
2. 템플릿 상속은 읽어온 문자열들의 조합입니다.
"""


# def index(request):
#     rendered = render_to_string("blog/hello.txt", {"name": "Django"})
#     print(rendered)
#     print(type(rendered))
#     name = "hojun"
#     s = f"<p>hello, {name}</p>"
#     # return HttpResponse(rendered)
#     return HttpResponse(s)
#     # return HttpResponse(rendered + s)


def index(request):
    rendered = render_to_string("blog/hello.txt", {"name": "Django"})
    name = "hojun"
    s = f"<p>hello, {name}</p>"
    return render(
        request, "blog/index.html", {"normal_string": s, "safe_string": rendered}
    )
