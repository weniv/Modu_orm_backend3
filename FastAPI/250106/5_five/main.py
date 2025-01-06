from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import os

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

# Serving할 디렉토리를 설정합니다.
# live server를 사용하면 굳이 안해도 됩니다.
STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 업로드된 파일을 저장할 디렉토리
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.post("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 파일 저장
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        return JSONResponse(
            content={
                "filename": file.filename,
                "message": "파일이 성공적으로 업로드되었습니다.",
            },
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"파일 업로드 중 오류가 발생했습니다: {str(e)}"},
            status_code=500,
        )


# 업로드된 파일 확인
@app.get("/files/")
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}
