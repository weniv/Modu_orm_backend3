from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates

# 블로그 포스트 데이터
blog_posts = [
    {
        "id": 1,
        "title": "첫번째 포스트",
        "contents": "첫번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-1",
    },
    {
        "id": 2,
        "title": "두번째 포스트",
        "contents": "두번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-2",
    },
    {
        "id": 3,
        "title": "세번째 포스트",
        "contents": "세번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-3",
    },
]

blog_notice = [
    {
        "id": 1,
        "title": "첫번째 공지",
        "contents": "첫번째 공지 내용입니다.",
        "author": "이호준",
        "date": "2025-1-1",
    },
    {
        "id": 2,
        "title": "두번째 공지",
        "contents": "두번째 공지 내용입니다.",
        "author": "이호준",
        "date": "2025-1-2",
    },
]

# FastAPI 애플리케이션 설정
app = FastAPI(
    title="Blog Application",
    description="FastAPI와 Jinja2를 사용한 블로그 애플리케이션",
    docs_url="/documentation",
    redoc_url=None,
)

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "recent_posts": blog_posts[-3:]}
    )


@app.get("/blog")
async def blog_list(request: Request):
    return templates.TemplateResponse(
        "blog.html", {"request": request, "posts": blog_posts[::-1], "title": "blog"}
    )


# 나중에 배웁니다. 함께 수정해봐요.
@app.get("/blog/{post_author}")
async def blog_post(request: Request, post_author: str):
    print(post_author)
    if post_author.isdigit():
        post = blog_posts[int(post_author) - 1]
        return templates.TemplateResponse(
            "post.html", {"request": request, "post": post}
        )
    else:
        filter_post = list(
            filter(lambda post: post["author"] == post_author, blog_posts)
        )[::-1]
        return templates.TemplateResponse(
            "blog.html", {"request": request, "posts": filter_post}
        )


# @app.get("/blog/{post_id}")
# async def blog_post(request: Request, post_id: int):
#     post = blog_posts[post_id - 1]
#     return templates.TemplateResponse("post.html", {"request": request, "post": post})


@app.get("/notice")
async def notice_list(request: Request):
    return templates.TemplateResponse(
        "blog.html",
        {"request": request, "posts": blog_notice[::-1], "title": "notice"},
    )


@app.get("/notice/{post_id}")
async def notice_post(request: Request, post_id: int):
    post = blog_notice[post_id - 1]
    return templates.TemplateResponse("post.html", {"request": request, "post": post})
