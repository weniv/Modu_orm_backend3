from fastapi import FastAPI


app = FastAPI()
# app = FastAPI(redirect_slashes=False)
# 이렇게 하면 뒤에 슬러시가 있는지 없는지 무조건 강제
# FastAPI는 기본적으로 trailing slash를 자동으로 처리합니다 (redirect_slashes=True)


@app.get("/")
def read_root():
    return {"URL": "/"}


# /abc, /abc/ 모두 접근 가능
@app.get("/abc")
def read_root():
    return {"URL": "/abc"}


@app.get("/abcd")
def read_root():
    """
    매핑 URL
    * /abcd
    * /abcd/
    * /abcd?age=10
    * (X) /abcde
    """
    return {"URL": "/abcd"}


@app.get("/abcd{tail}")
def read_root(tail: str = ""):
    """
    매핑 URL
    * /abcd/
    * /abcde
    * abcde?age=10/
    """
    return {"URL": f"/abcd{tail}"}


# /abcde/로 접근하면 아래 URL로 매핑
@app.get("/abcd{tail}/")
def read_root(tail: str = ""):
    """
    매핑 URL
    * /abcde/
    """
    print(f"tail: {tail}")
    return {"URL": f"/abcd{tail}/success"}
