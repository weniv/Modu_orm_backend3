from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

blog_post = [
    {
        "title": "첫번째 포스트",
        "contents": "첫번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-1",
    },
    {
        "title": "두번째 포스트",
        "contents": "두번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-2",
    },
    {
        "title": "세번째 포스트",
        "contents": "세번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-3",
    },
]

"""
/ -> index.html, 소개가 들어갑니다.
/blog -> blog.html, 블로그 포스트 목록이 들어갑니다.
/blog/{post_id} -> post.html, 블로그 포스트 내용이 들어갑니다. post_id는 1부터 시작합니다. blog/1이라고 입력하면 0번째 게시물이 나옵니다.

jinja2사용해서 웹 페이지를 만들려고 하는데 아래 코드가 기본 코드야. 이 코드를 기반으로 우선 main.py를 작성해줘.
"""


app = FastAPI(docs_url="/documentation", redoc_url=None)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
