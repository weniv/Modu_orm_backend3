from fastapi import FastAPI

app = FastAPI()

# URL        | Method | 설명
# -----------|--------|----------------------
# /blog      | GET    | 블로그 목록을 가져온다.(V)
# /blog/{id} | GET    | 블로그 상세 정보를 가져온다.(V)
# /blog      | POST   | 블로그를 생성한다.(V)
# /blog/{id} | PUT    | 블로그를 수정한다.(V)
# /blog/{id} | DELETE | 블로그를 삭제한다.(V)


"""
부족한 부분
1. 실제 DB를 사용하지 않았다.
2. 모델을 사용하지 않았다.
3. 인증을 체크하지 않았다.
    3.1 Delete, Put, Post는 인증이 필요하다.
"""

# 데이터베이스 역할을 하는 리스트
blog_data = [
    {"id": 1, "title": "Blog Title 1", "content": "Content 1", "author": "Author 1"},
    {"id": 2, "title": "Blog Title 2", "content": "Content 2", "author": "Author 1"},
    {"id": 3, "title": "Blog Title 3", "content": "Content 3", "author": "Author 2"},
    {"id": 4, "title": "Blog Title 4", "content": "Content 4", "author": "Author 2"},
    {"id": 5, "title": "Blog Title 5", "content": "Content 5", "author": "Author 3"},
    {"id": 6, "title": "Blog Title 6", "content": "Content 6", "author": "Author 3"},
]


@app.get("/blog")
def get_blogs():
    return blog_data


@app.get("/blog/{id}")
def get_blog(id: int):
    for blog in blog_data:
        if blog["id"] == id:
            return blog
    return {"status": "Not Found"}


"""
블로그 생성은 왜 POST고, GET은 안되나요?
GET도 포스트 생성이 되게 할 수 있습니다. 다만, Body에 데이터를 담아 보내야 하는데
이렇게 하는 경우에는 보통 POST를 사용합니다.
"""


@app.post("/blog")
def create_blog(blog_dict: dict):
    new_id = blog_data[-1]["id"] + 1
    new_blog = {
        "id": new_id,
        "title": blog_dict.get("title"),
        "content": blog_dict.get("content"),
        "author": blog_dict.get("author"),
    }
    blog_data.append(new_blog)
    return new_blog


@app.put("/blog/{id}")
def update_blog(id: int, blog_update: dict):
    for blog in blog_data:
        if blog["id"] == id:
            blog.update(blog_update)
            return blog
    return {"status": "Not Found"}


@app.delete("/blog/{id}")
def delete_blog(id: int):
    for idx, blog in enumerate(blog_data):
        if blog["id"] == id:
            return blog_data.pop(idx)
    return {"status": "Not Found"}
