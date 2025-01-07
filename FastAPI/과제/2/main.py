from fastapi import FastAPI, HTTPException, Depends  # FastAPI의 핵심 클래스 및 의존성 관리 도구, HTTP 예외 처리 임포트
from fastapi.staticfiles import StaticFiles  # 정적 파일 제공을 위한 도구 임포트
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 임포트
from typing import List  # 리스트 타입을 명시하기 위한 typing 모듈 추가
from pydantic import BaseModel  # 요청 및 응답 데이터 검증을 위한 모델 정의 도구 임포트
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func  # SQLAlchemy의 ORM 및 데이터베이스 관련 클래스와 함수 임포트
from sqlalchemy.ext.declarative import declarative_base  # 베이스 클래스 생성 도구 임포트
from sqlalchemy.orm import sessionmaker, Session  # 데이터베이스 세션 관리를 위한 도구 임포트
import datetime  # 날짜 및 시간을 다루기 위한 파이썬 내장 모듈 임포트
import os  # 운영체제와 상호작용하기 위한 파이썬 내장 모듈 임포트

# 데이터베이스 설정
DATABASE_URL = "sqlite:///./test.db"  # SQLite 데이터베이스 파일 경로 설정
engine = create_engine(DATABASE_URL)  # SQLAlchemy 엔진 생성, 데이터베이스와의 연결 관리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 세션 팩토리 생성, 세션 관리를 담당
Base = declarative_base()  # 모든 모델이 상속받을 수 있는 베이스 클래스 정의

# 모델 정의
class Blog(Base):
    __tablename__ = "blogs"  # 데이터베이스 테이블 이름 설정
    id = Column(Integer, primary_key=True, index=True)  # 기본 키 설정 및 인덱스 추가 (검색 최적화)
    title = Column(String)  # 제목 필드, 문자열 타입
    content = Column(String)  # 내용 필드, 문자열 타입
    author = Column(String)  # 작성자 필드, 문자열 타입
    created_at = Column(DateTime, default=func.now())  # 생성 시간 필드, 기본값은 현재 시간
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 수정 시간 필드, 기본값은 현재 시간, 수정 시 자동 업데이트

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)  # 정의된 테이블을 데이터베이스에 생성

# Pydantic 모델 정의
class BlogCreate(BaseModel):  # 블로그 생성 요청 데이터 검증을 위한 모델
    title: str  # 제목 필수 입력
    content: str  # 내용 필수 입력

class BlogUpdate(BaseModel):  # 블로그 수정 요청 데이터 검증을 위한 모델
    title: str  # 제목 필수 입력
    content: str  # 내용 필수 입력

class BlogResponse(BaseModel):  # 블로그 응답 데이터 검증 및 직렬화를 위한 모델
    id: int  # ID 필드
    title: str  # 제목 필드
    content: str  # 내용 필드
    author: str  # 작성자 필드
    created_at: datetime.datetime  # 생성 시간 필드
    updated_at: datetime.datetime  # 수정 시간 필드

    class Config:
        orm_mode = True  # SQLAlchemy 객체를 직접 Pydantic 모델로 변환 가능

# FastAPI 앱 설정
app = FastAPI()  # FastAPI 애플리케이션 인스턴스 생성

# static 폴더 경로 설정
if not os.path.exists("static"):  # static 폴더가 없으면
    os.mkdir("static")  # static 폴더 생성
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS 설정
app.add_middleware(  # 미들웨어 추가
    CORSMiddleware,  # CORS 미들웨어 사용
    allow_origins=["*"],  # 모든 오리진 허용
    allow_credentials=True,  # 자격 증명 허용
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# DB 세션 의존성
def get_db():  # 데이터베이스 세션 관리 함수
    db = SessionLocal()  # 세션 생성
    try:
        yield db  # 요청이 끝날 때까지 세션 유지
    finally:
        db.close()  # 요청 종료 후 세션 닫기

# 블로그 목록 조회
@app.get("/blogs", response_model=List[BlogResponse])  # GET 요청을 처리하고 응답 모델 지정
def read_blogs(db: Session = Depends(get_db)):  # 의존성 주입을 통해 세션 관리
    return db.query(Blog).all()[::-1]  # 모든 블로그를 최신순으로 조회

# 블로그글 조회
@app.get("/blogs/{blog_id}", response_model=BlogResponse)  # 특정 블로그 조회 엔드포인트
def read_blog(blog_id: int, db: Session = Depends(get_db)):  # 블로그 ID와 세션을 매개변수로 받음
    blog = db.query(Blog).filter(Blog.id == blog_id).first()  # ID로 블로그 조회
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")  # 블로그가 없으면 404 예외 발생
    return blog  # 결과 반환

# 블로그글 생성
@app.post("/blogs", response_model=BlogResponse)  # 블로그 생성 엔드포인트
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):  # 입력 데이터와 세션 관리
    new_blog = Blog(**blog.model_dump())  # Pydantic 모델을 딕셔너리로 변환 후 객체 생성
    new_blog.author = "admin"  # 작성자는 고정값
    db.add(new_blog)  # 세션에 객체 추가
    db.commit()  # 변경 사항 커밋
    db.refresh(new_blog)  # 최신 상태로 객체 갱신
    return new_blog  # 생성된 블로그 반환

# 블로그글 수정
@app.put("/blogs/{blog_id}", response_model=BlogResponse)  # 블로그 수정 엔드포인트
def update_blog(blog_id: int, blog: BlogUpdate, db: Session = Depends(get_db)):  # 수정 요청 처리
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()  # ID로 블로그 조회
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")  # 블로그가 없으면 404 예외 발생
    for key, value in blog.model_dump().items():  # 입력된 필드만 업데이트
        setattr(db_blog, key, value)
    db.commit()  # 변경 사항 커밋
    db.refresh(db_blog)  # 최신 상태로 갱신
    return db_blog  # 수정된 블로그 반환

# 블로그글 삭제
@app.delete("/blogs/{blog_id}")  # 블로그 삭제 엔드포인트
def delete_blog(blog_id: int, db: Session = Depends(get_db)):  # 삭제 요청 처리
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()  # ID로 블로그 조회
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")  # 블로그가 없으면 404 예외 발생
    db.delete(db_blog)  # 데이터 삭제
    db.commit()  # 변경 사항 커밋
    return {"message": "Deleted successfully"}  # 성공 메시지 반환
