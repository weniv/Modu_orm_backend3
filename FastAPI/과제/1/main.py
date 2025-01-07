from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# DB 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./blogs.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# DB 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SQLAlchemy 모델 기본 클래스 생성
Base = declarative_base()


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


# DB 테이블 생성
Base.metadata.create_all(bind=engine)


# DB 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BlogCreate(BaseModel):
    title: str
    author: str
    content: str


class BlogUpdate(BaseModel):
    title: str
    author: str
    content: str | None = ""


class BlogResponse(BlogCreate):
    id: int


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


def init_db():
    db = SessionLocal()

    if not db.query(Blog).all():
        for data in [
            {
                "title": "Django",
                "author": "django_author",
                "content": "aaa",
            },
            {
                "title": "FastAPI",
                "author": "fastapi_author",
                "content": "bbb",
            },
            {
                "title": "Python",
                "author": "python_author",
                "content": "ccc",
            },
        ]:
            current_time = datetime.now()
            db.add(Blog(**data, created_at=current_time, updated_at=current_time))
            db.commit()

    db.close()


init_db()


@app.post("/blogs")
def create_blog(blog_create_data: BlogCreate, db: Session = Depends(get_db)):
    current_time = datetime.now()
    new_blog = Blog(
        **blog_create_data.model_dump(),
        created_at=current_time,
        updated_at=current_time
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blogs", response_model=list[BlogResponse])
def read_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).all()


@app.get("/blogs/{blog_id}", response_model=BlogResponse)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.put("/blogs/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: int, blog_update_data: BlogUpdate, db: Session = Depends(get_db)
):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # 아래처럼 그냥 넣으면 Pylance 에러 발생
    # blog.title = blog_update_data.title
    # blog.author = blog_update_data.author
    # blog.content = blog_update_data.content
    for k, v in blog_update_data.model_dump().items():
        setattr(blog, k, v)
    setattr(blog, "updated_at", datetime.now())

    db.commit()
    db.refresh(blog)
    return blog


@app.delete("/blogs/{blog_id}", response_model=BlogResponse)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(blog)
    db.commit()
    return blog
