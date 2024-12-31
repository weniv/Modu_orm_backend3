from fastapi import FastAPI, Depends, HTTPException  # FastAPI 프레임워크 핵심 컴포넌트
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
)  # SQLAlchemy ORM 컴포넌트
from sqlalchemy.ext.declarative import declarative_base  # SQLAlchemy 모델 기본 클래스
from sqlalchemy.orm import sessionmaker, Session  # 데이터베이스 세션 관리
from pydantic import BaseModel  # 데이터 검증을 위한 Pydantic 모델

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"  # SQLite 데이터베이스 URL 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },  # SQLite는 단일 스레드만 지원하므로 이 옵션 필요
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 데이터베이스 세션 팩토리 생성
"""
이 코드가 DB와 직접 연결되는 코드! 각 함수마다 별도의 세션을 생성하고 종료함!

# autocommit=True 일 경우
db.add(item)  # 즉시 데이터베이스에 반영됨

# autocommit=False 일 경우 (권장)
db.add(item)  # 세션에만 추가됨
db.commit()   # 명시적으로 커밋해야 데이터베이스에 반영됨

# autoflush=True 일 경우
item = Item(name="test")
db.add(item)
# 쿼리 실행 시 자동으로 flush 발생
db.query(Item).all()  

# autoflush=False 일 경우
item = Item(name="test")
db.add(item)
db.flush()  # 명시적으로 flush 호출 필요
db.query(Item).all()

# bind=engine은 연결 엔진 설정
"""

Base = declarative_base()  # SQLAlchemy 모델의 기본 클래스 생성


# SQLAlchemy 모델 정의 (데이터베이스 테이블 구조)
class Item(Base):
    __tablename__ = "items"  # 실제 데이터베이스 테이블 이름
    id = Column(Integer, primary_key=True, index=True)  # 기본키, 자동 증가
    name = Column(String, index=True)  # 검색을 위한 인덱스가 있는 이름 필드
    description = Column(String, index=True)  # 검색을 위한 인덱스가 있는 설명 필드
    price = Column(Float)  # 가격 필드 (소수점 지원)


# 정의된 모델을 기반으로 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)
"""
Base.metadata.create_all(bind=engine)은 실제 데이터베이스에 테이블을 생성하는 코드입니다.
CREATE TABLE items (
    id INTEGER NOT NULL, 
    name VARCHAR, 
    description VARCHAR,
    price FLOAT,
    PRIMARY KEY (id)
)
"""


# Pydantic 모델 정의 (입력 데이터 검증)
class ItemCreate(BaseModel):
    name: str
    description: str | None = None  # 선택적 필드 (None 허용)
    price: float


class ItemUpdate(BaseModel):
    name: str
    description: str | None = None
    price: float | None = None


# Pydantic 응답 모델 정의 (출력 데이터 형식)
class ItemResponse(ItemCreate):
    id: int  # 데이터베이스에서 생성된 ID 포함


app = FastAPI()  # FastAPI 애플리케이션 인스턴스 생성


# 데이터베이스 세션 의존성 함수
def get_db():
    db = SessionLocal()  # 새로운 데이터베이스 세션 생성
    try:
        yield db  # 세션을 라우트 핸들러에 제공
    finally:
        db.close()  # 요청 처리 완료 후 세션 종료


# CRUD 작업을 위한 엔드포인트들
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())  # Pydantic 모델을 SQLAlchemy 모델로 변환
    db.add(db_item)  # 새 아이템을 세션에 추가
    db.commit()  # 변경사항을 데이터베이스에 커밋
    db.refresh(db_item)  # 데이터베이스에서 아이템 새로고침 (자동생성된 ID 등 포함)
    return db_item  # 생성된 아이템 반환


@app.get("/items/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()  # 모든 아이템 조회


@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()  # ID로 특정 아이템 조회
    if db_item is None:  # 아이템이 없으면 404 에러 발생
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item  # 찾은 아이템 반환


@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    # 삭제할 아이템을 데이터베이스에서 조회
    db_item = db.query(Item).filter(Item.id == item_id).first()

    # 아이템이 존재하지 않으면 404 에러 발생
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # 조회된 아이템을 세션에서 삭제
    db.delete(db_item)

    # 변경사항을 데이터베이스에 커밋
    db.commit()

    # 삭제된 아이템 정보 반환
    return db_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    # 업데이트할 아이템을 데이터베이스에서 조회
    db_item = db.query(Item).filter(Item.id == item_id).first()

    # 아이템이 존재하지 않으면 404 에러 발생
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # 아이템 정보 업데이트
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price

    # 변경사항을 데이터베이스에 커밋
    db.commit()

    # 업데이트된 아이템 정보 반환
    return db_item
