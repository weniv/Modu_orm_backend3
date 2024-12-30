"""
블로그 포스트를 생성하는 엔드포인트를 만들어보세요. 블로그 포스트는 제목, 내용, 작성자 정보(이름, 이메일)를 포함해야 합니다. 중첩된 Pydantic 모델을 사용하세요.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
blogs = []


class User(BaseModel):
    name: str
    email: str


class Blog(BaseModel):
    title: str
    content: str
    author: User


@app.get("/blog")
async def blog_list():
    return {"items": blogs}


@app.post("/blog/create")
async def blog_create(blog: Blog):
    blogs.append(blog)
    return {"blog": blog}


"""
{
    "title": "hello 1",
    "content": "world 1",
    "author": {
      "name": "hojun",
      "email": "hojun@gmail.com"
    }
}
"""
