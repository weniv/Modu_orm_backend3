from fastapi import FastAPI


app = FastAPI()


thumnail = ["위니브1.png", "위니브2.png", "위니브3.png"]
employee = ["김철수", "홍길동", "김영희"]

contact = {
    "phone": "010-1234-5678",
    "email": "paullab@naver.com",
    "address": "제주시 첨단로 330",
}


@app.get("/")
def read_root():
    return {"message": "위니브에 오신것을 환영합니다.", "thumbnail": thumnail}


@app.get("/about")
def read_about():
    return {"message": "위니브는 위대한 회사입니다.", "employee": employee}


@app.get("/contact")
def read_contact():
    return {
        "message": "위니브에 문의하세요.",
        "phone": contact["phone"],
        "email": contact["email"],
        "address": contact["address"],
    }


@app.get("/a")
def read_a():
    return {"message": "A 페이지입니다."}


@app.get("/b")
def read_b():
    return {"message": "B 페이지입니다."}
