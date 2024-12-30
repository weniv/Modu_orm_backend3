from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Union

app = FastAPI()


# Pydantic 모델 정의
class Item(BaseModel):
    name: str
    price: float


class Message(BaseModel):
    message: str


# 메모리에 데이터를 저장할 리스트
items = []


@app.post(
    "/item/",
    response_model=Item,  # 어떤 모델로 응답할지를 결정
    status_code=status.HTTP_201_CREATED,  # 상태 코드를 결정
    # response_model_exclude={"price"},  # 응답에서 제외할 필드를 결정
    response_model_include={"name", "price"},  # 응답에서 포함할 필드를 결정
)
async def create_item(item: Item):
    items.append(item)
    return item


@app.get("/item/")
async def read_item():
    return items


@app.get(
    "/item/",
    # status_code=status.HTTP_200_OK,
    status_code=404,  # 실제 주는 데이터와 다를 수도 있습니다.
)
async def create_item():
    return {"hello": "world"}


@app.get("/item/{item_id}", response_model=Union[Item, Message])
async def read_item(item_id: int):
    if item_id == 1:
        return items[item_id - 1]
    else:
        return Message(message="Item not found")


@app.get("/not_found")
def read_items():
    return HTTPException(status_code=404, detail="Not Found")


@app.get("/found")
def read_items():
    return {"detail": "Found"}


@app.get("/server_error")
def read_items():
    return HTTPException(status_code=500, detail="Server Error")
