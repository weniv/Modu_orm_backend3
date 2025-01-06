from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # 모든 URL에서 접근 허용, 실무에서는 내 서비스 도메인만 넣어주시면 됩니다.
    # admin은 보통 다른 URL에서 접근하도록 합니다. /admin, admin.example.com 사용하지 않습니다.
    allow_credentials=True,  # 쿠키 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


blogs = [
    {
        "id": 1,
        "title": "Hello",
        "content": "World",
        "author": "admin",
        "created_at": "2025-01-06",
        "updated_at": "2025-01-06",
    },
    {
        "id": 2,
        "title": "FastAPI",
        "content": "Python",
        "author": "admin",
        "created_at": "2025-01-07",
        "updated_at": "2025-01-07",
    },
    {
        "id": 3,
        "title": "Django",
        "content": "Python",
        "author": "admin",
        "created_at": "2025-01-08",
        "updated_at": "2025-01-08",
    },
]


# 블로그 글 목록 조회
@app.get("/blogs")
def read_blogs():
    reversed_data = blogs[::-1]
    return reversed_data


# 블로그 글 상세 조회
@app.get("/blogs/{blog_id}")
def read_blog(blog_id: int):
    # 삭제될 수 있으므로 그냥 인덱스로 조회해서는 안됩니다.
    for blog in blogs:
        if blog["id"] == blog_id:
            return blog
    return {"message": "Not Found"}


class BlogCreate(BaseModel):
    title: str
    content: str


# 블로그 글 생성
@app.post("/blogs")
def create_blog(blog_create_data: BlogCreate):
    # datetime 객체를 통해 현재 시간을 가져와서 문자로 할당하도록 하겠습니다.
    print("들어오긴 했음")
    import datetime

    now = datetime.datetime.now()
    created_at = now.strftime("%Y-%m-%d")

    # 여기에 id 부분은 len보다는 id의 최댓값으로 설정하는 것이 좋습니다.
    # 다만 이 부분은 데이터베이스를 사용하지 않아서 이렇게 처리하였습니다.
    blog = {
        "id": len(blogs) + 1,
        "title": blog_create_data.title,
        "content": blog_create_data.content,
        "author": "admin",
        "created_at": created_at,
        "updated_at": created_at,
    }
    blogs.append(blog)
    return blog


class BlogUpdate(BaseModel):
    title: str
    content: str


# 블로그 글 수정
@app.put("/blogs/{blog_id}")
def update_blog(blog_id: int, blog_update_data: BlogUpdate):
    print(blog_id, blog_update_data)
    for blog in blogs:
        if blog["id"] == blog_id:
            blog["title"] = blog_update_data.title
            blog["content"] = blog_update_data.content
            # 수정 시간을 업데이트
            import datetime

            now = datetime.datetime.now()
            updated_at = now.strftime("%Y-%m-%d")
            blog["updated_at"] = updated_at
            return blog
    return {"message": "Not Found"}


# 블로그 글 삭제
@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int):
    for blog in blogs:
        if blog["id"] == blog_id:
            blogs.remove(blog)
            return {"message": "Deleted"}
    return {"message": "Not Found"}
