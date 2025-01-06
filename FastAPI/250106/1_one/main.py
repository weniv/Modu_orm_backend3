from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

items = [
    {"name": "hello", "price": 50.2},
    {"name": "world", "price": 62.5},
]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return items[item_id - 1]
