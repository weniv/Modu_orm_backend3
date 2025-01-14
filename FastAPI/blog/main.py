import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from fastapi.security.api_key import APIKeyHeader


# 정적 파일 디렉토리 생성
if not os.path.exists("static"):
    os.makedirs("static")

# Database 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./blogs.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT 설정
SECRET_KEY = "your-secret-key"  # 실제 운영환경에서는 환경변수로 관리
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Database Models
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    blogs = relationship("BlogModel", back_populates="author")


class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    author = relationship("UserModel", back_populates="blogs")


# Pydantic Models
class UserCreate(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: int
    email: str
    created_at: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class BlogCreate(BaseModel):
    title: str
    content: str


class BlogUpdate(BaseModel):
    title: str
    content: str


class Blog(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

auth_header = APIKeyHeader(name="Authorization", auto_error=False)
app = FastAPI(
    dependencies=[Depends(auth_header)],
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Utility Functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# Dependencies
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


# 초기 데이터 삽입 함수
def init_db():
    db = SessionLocal()
    try:
        # 데이터가 없을 경우에만 초기 데이터 삽입
        if not db.query(BlogModel).first():
            # 먼저 테스트 사용자 생성
            test_user = UserModel(
                email="test@example.com",
                hashed_password=get_password_hash("testpassword"),
                created_at="2025-01-06",
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)

            # 테스트 블로그 포스트 생성
            initial_data = [
                BlogModel(
                    title="Hello",
                    content="World",
                    author_id=test_user.id,
                    created_at="2025-01-06",
                    updated_at="2025-01-06",
                ),
                BlogModel(
                    title="FastAPI",
                    content="Python",
                    author_id=test_user.id,
                    created_at="2025-01-07",
                    updated_at="2025-01-07",
                ),
                BlogModel(
                    title="Django",
                    content="Python",
                    author_id=test_user.id,
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


# Authentication Endpoints
@app.post("/register", response_model=User)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 체크
    db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 비밀번호 해싱
    hashed_password = get_password_hash(user_data.password)

    # 사용자 생성
    db_user = UserModel(
        email=user_data.email,
        hashed_password=hashed_password,
        created_at=datetime.now().strftime("%Y-%m-%d"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Blog Endpoints
@app.get("/blogs", response_model=list[Blog])
def read_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).order_by(BlogModel.id.desc()).all()
    return blogs


@app.get("/blogs/{blog_id}", response_model=Blog)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.post("/blogs", response_model=Blog)
def create_blog(
    blog_create_data: BlogCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    now = datetime.now().strftime("%Y-%m-%d")
    new_blog = BlogModel(
        title=blog_create_data.title,
        content=blog_create_data.content,
        author_id=current_user.id,
        created_at=now,
        updated_at=now,
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(
    blog_id: int,
    blog_update_data: BlogUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this blog"
        )

    blog.title = blog_update_data.title
    blog.content = blog_update_data.content
    blog.updated_at = datetime.now().strftime("%Y-%m-%d")

    db.commit()
    db.refresh(blog)

    return blog


@app.delete("/blogs/{blog_id}")
def delete_blog(
    blog_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this blog"
        )

    db.delete(blog)
    db.commit()

    return {"message": "Blog deleted successfully"}
