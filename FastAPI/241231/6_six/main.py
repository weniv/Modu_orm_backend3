# FastAPI 프레임워크와 필요한 의존성들을 임포트
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)  # OAuth2 인증 관련 클래스
from pydantic import BaseModel  # 데이터 검증을 위한 Pydantic 모델
from datetime import datetime, timedelta  # 시간 관련 처리를 위한 클래스
from jose import jwt  # JWT 토큰 생성 및 검증을 위한 라이브러리

# FastAPI 인스턴스 생성
app = FastAPI()

# JWT 토큰 생성에 필요한 기본 설정값들
SECRET_KEY = "your-secret-key"  # JWT 서명에 사용될 비밀키
ALGORITHM = "HS256"  # JWT 암호화 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 유효 기간 (분)

# 임시 사용자 저장소 (실제 프로덕션에서는 데이터베이스 사용 필요)
users_db = {}

# OAuth2 인증 스키마 설정 - 토큰 엔드포인트 URL 지정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 사용자 데이터 검증을 위한 Pydantic 모델
class User(BaseModel):
    username: str  # 사용자 이름
    password: str  # 비밀번호


# 토큰 응답 데이터 검증을 위한 Pydantic 모델
class Token(BaseModel):
    access_token: str  # JWT 토큰 문자열
    token_type: str  # 토큰 타입 (bearer)


# JWT 토큰 생성 함수
def create_token(username: str):
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )  # 만료 시간 설정
    token_data = {"sub": username, "exp": expire}  # 토큰에 포함될 데이터
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)  # JWT 토큰 생성


# 현재 사용자 인증 함수 - 보호된 라우트에서 사용
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # JWT 토큰 디코딩 및 검증
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")  # 토큰에서 사용자 이름 추출
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.JWTError:  # JWT 토큰 검증 실패시
        raise HTTPException(status_code=401, detail="Invalid token")


# 회원가입 엔드포인트
@app.post("/signup")
async def signup(user: User):
    if user.username in users_db:  # 이미 존재하는 사용자인지 확인
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = user.password  # 사용자 정보 저장
    print(users_db)
    return {"message": "User created successfully"}


# 로그인 및 토큰 발급 엔드포인트
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 사용자 인증
    user_password = users_db.get(form_data.username)
    if not user_password or user_password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # 인증 성공시 JWT 토큰 생성 및 반환
    access_token = create_token(form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


# 보호된 라우트 예시 - 인증된 사용자만 접근 가능
@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}! This is a protected route"}
