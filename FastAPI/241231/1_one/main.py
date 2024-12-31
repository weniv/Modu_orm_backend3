# 필요한 라이브러리 임포트
from fastapi import (
    FastAPI,
    HTTPException,
)  # FastAPI 프레임워크와 예외처리를 위한 클래스
from pydantic import BaseModel  # 데이터 검증을 위한 Pydantic 기본 모델
from typing import List, Optional  # 타입 힌팅을 위한 타입들

# FastAPI 인스턴스 생성
app = FastAPI()

# 메모리 내 데이터 저장소 (데이터베이스 대신 임시로 사용)
items = {}


# 기본 아이템 모델 정의
class Item(BaseModel):
    name: str  # 필수 문자열 필드
    description: str | None = None  # 선택적 문자열 필드, 기본값은 None
    price: float  # 필수 실수 필드


# 아이템 업데이트용 모델 정의
class ItemUpdate(BaseModel):
    # 모든 필드가 선택적(Optional)이므로 부분 업데이트 가능
    name: str | None = None
    description: str | None = None
    price: float | None = None


# CREATE - 아이템 생성 엔드포인트
@app.post("/items/{item_id}", response_model=Item)
def create_item(item_id: int, item: Item):
    # 이미 존재하는 아이템 ID인 경우 400 에러 발생
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    # 새 아이템 저장
    items[item_id] = item
    return item


# READ - 모든 아이템 조회 엔드포인트
@app.get("/items", response_model=List[Item])
def read_items():
    # dictionary values를 리스트로 변환하여 반환
    return list(items.values())


# UPDATE - 아이템 업데이트 엔드포인트
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    # 존재하지 않는 아이템 ID인 경우 404 에러 발생
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    # 기존 아이템 조회
    stored_item = items[item_id]

    # 업데이트할 데이터만 추출 (설정되지 않은 필드는 제외)
    update_data = item.dict(exclude_unset=True)

    # 기존 아이템을 복사하고 새로운 데이터로 업데이트
    updated_item = stored_item.copy(update=update_data)

    # 업데이트된 아이템 저장
    items[item_id] = updated_item

    return updated_item


# DELETE - 아이템 삭제 엔드포인트
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    # 존재하지 않는 아이템 ID인 경우 404 에러 발생
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    # 아이템을 삭제하고 삭제된 아이템 반환
    # pop() 메서드는 키를 삭제하고 해당 값을 반환
    item = items.pop(item_id)
    return item
