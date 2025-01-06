from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime

# Database 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./blogs.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Blog 모델 정의
class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)


# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic 모델
class BlogCreate(BaseModel):
    title: str
    content: str


class Blog(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# 초기 데이터 삽입 함수
def init_db():
    db = SessionLocal()
    try:
        # 데이터가 없을 경우에만 초기 데이터 삽입
        if not db.query(BlogModel).first():
            initial_data = [
                BlogModel(
                    title="Hello",
                    content="World",
                    author="admin",
                    created_at="2025-01-06",
                    updated_at="2025-01-06",
                ),
                BlogModel(
                    title="FastAPI",
                    content="Python",
                    author="admin",
                    created_at="2025-01-07",
                    updated_at="2025-01-07",
                ),
                BlogModel(
                    title="Django",
                    content="Python",
                    author="admin",
                    created_at="2025-01-08",
                    updated_at="2025-01-08",
                ),
            ]
            for data in initial_data:
                db.add(data)
            db.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


# 애플리케이션 시작 시 초기 데이터 삽입
init_db()


# 블로그 글 목록 조회
@app.get("/blogs", response_model=list[Blog])
def read_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).order_by(BlogModel.id.desc()).all()
    return blogs


# 블로그 글 생성
@app.post("/blogs", response_model=Blog)
def create_blog(blog_create_data: BlogCreate, db: Session = Depends(get_db)):
    now = datetime.datetime.now()
    created_at = now.strftime("%Y-%m-%d")
    print(blog_create_data)

    new_blog = BlogModel(
        title=blog_create_data.title,
        content=blog_create_data.content,
        author="admin",
        created_at=created_at,
        updated_at=created_at,
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog
