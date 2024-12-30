from fastapi import FastAPI, HTTPException

app = FastAPI()

# 데이터베이스 역할을 하는 리스트
blog_data = [
    {"id": 1, "title": "Blog Title 1", "content": "Content 1", "author": "Author 1"},
    {"id": 2, "title": "Blog Title 2", "content": "Content 2", "author": "Author 1"},
    {"id": 3, "title": "Blog Title 3", "content": "Content 3", "author": "Author 2"},
    {"id": 4, "title": "Blog Title 4", "content": "Content 4", "author": "Author 2"},
    {"id": 5, "title": "Blog Title 5", "content": "Content 5", "author": "Author 3"},
    {"id": 6, "title": "Blog Title 6", "content": "Content 6", "author": "Author 3"},
]


# GET /blog - 블로그 목록 조회
@app.get("/blog")
def get_blogs():
    return blog_data


# GET /blog/{id} - 특정 블로그 조회
@app.get("/blog/{blog_id}")
def get_blog(blog_id: int):
    blog = next((blog for blog in blog_data if blog["id"] == blog_id), None)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


# POST /blog - 새로운 블로그 생성
@app.post("/blog")
def create_blog(blog_dict: dict):
    new_id = blog_data[-1]["id"] + 1 if blog_data[-1] else 0
    new_blog = {
        "id": new_id,
        "title": blog_dict.get("title"),
        "content": blog_dict.get("content"),
        "author": blog_dict.get("author"),
    }
    blog_data.append(new_blog)
    return new_blog


# PUT /blog/{id} - 블로그 수정
@app.put("/blog/{blog_id}")
def update_blog(blog_id: int, blog_update: dict):
    blog_idx = next(
        (idx for idx, blog in enumerate(blog_data) if blog["id"] == blog_id), None
    )
    if blog_idx is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_data[blog_idx].update(
        {
            "title": blog_update.get("title"),
            "content": blog_update.get("content"),
            "author": blog_update.get("author"),
        }
    )
    return blog_data[blog_idx]


# DELETE /blog/{id} - 블로그 삭제
@app.delete("/blog/{blog_id}")
def delete_blog(blog_id: int):
    blog_idx = next(
        (idx for idx, blog in enumerate(blog_data) if blog["id"] == blog_id), None
    )
    if blog_idx is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_data.pop(blog_idx)
    return {"message": "Blog deleted successfully"}


@app.get("/gettest")
def read_root():
    return {"Hello": "GET"}


@app.post("/posttest")
def read_root():
    return {"Hello": "POST"}
