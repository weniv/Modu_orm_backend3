from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    print("hello world")
    return {"Hello": "World"}


@app.get("/about")
def read_about():
    return {
        "title": "위니브 홈페이지",
        "description": "위니브 홈페이지입니다.",
        "contents": "위니브는.....",
    }


@app.get("/contact")
def read_contact():
    return {
        "title": "위니브 본사",
        "description": "위니브 본사입니다.",
        "contents": "위니브 본사는 제주특별자치도 제주시 첨단로 330",
    }
