from fastapi import FastAPI

app = FastAPI()


# 127.0.0.1:8000/items?skip=0&limit=10
@app.get("/items")
async def read_items(skip: int = 0, limit: int = 10, q: str | None = None):
    print(skip, limit)
    if q:
        # 보통 여기에 검색 코드를 작성합니다.
        return {"q": q, "skip": skip, "limit": limit}
    return {"skip": skip, "limit": limit}
