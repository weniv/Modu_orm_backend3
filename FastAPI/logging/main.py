from fastapi import FastAPI
import logging
from logging import FileHandler

# 로깅 설정
# DEBUG > INFO > WARNING > ERROR > CRITICAL
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 핸들러 추가
# 주석처리하면 파일로 쓰지 않습니다.
file_handler = FileHandler("logs.txt")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger = logging.getLogger()
logger.addHandler(
    file_handler
)  # 여기에 별도 구현한 핸들러를 추가하여 로그를 DB에 저장할 수 있습니다.

# FastAPI 앱 생성
app = FastAPI()


@app.get("/")
async def read_root():
    logging.info("루트 경로가 호출되었습니다")
    return {"message": "안녕하세요"}


@app.get("/test/info")
async def read_root():
    logging.info("test/info 경로가 호출되었습니다")
    return {"message": "안녕하세요"}


@app.get("/test/error")
async def read_root():
    logging.error("test/error 경로가 호출되었습니다")
    return {"message": "안녕하세요"}


@app.get("/test/debug")
async def read_root():
    logging.debug("test/debug 경로가 호출되었습니다")
    return {"message": "안녕하세요"}


@app.get("/test/warning")
async def read_root():
    logging.warning("test/warning 경로가 호출되었습니다")
    return {"message": "안녕하세요"}


@app.get("/test/critical")
async def read_root():
    logging.critical("test/critical 경로가 호출되었습니다")
    return {"message": "안녕하세요"}
