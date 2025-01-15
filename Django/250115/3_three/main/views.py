from django.shortcuts import render
from datetime import datetime


def index(request):
    context = {
        "user": {
            "name": "홍길동",
            "email": "hong@example.com",
            "age": 25,
        },
        "posts": [
            {
                "title": "첫 번째 글",
                "content": "aa bb cc dd ee ff gg",
                "date": datetime(2023, 7, 1),
            },
            {
                "title": "두 번째 글",
                "content": "반갑습니다.\n두 번째 글입니다.",
                "date": datetime(2023, 7, 15),
            },
            {
                "title": "세 번째 글",
                "content": "안녕히 가세요.\n세 번째 글입니다.",
                "date": datetime(2023, 7, 30),
            },
        ],
        "numbers": range(1, 11),
    }
    return render(request, "main/index.html", context)
