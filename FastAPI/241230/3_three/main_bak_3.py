from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
items = []


class Item(BaseModel):
    name: str
    price: float = 0


@app.get("/item")
async def item_list():
    return {"items": items}


@app.post("/item/create")
async def item_create(item: Item):
    items.append(item)
    return {"item": item}


@app.get("/item/{item_id}")
async def item_detail(item_id: int):
    try:
        item = items[item_id - 1]
    except IndexError:
        return {"error": "Item not found"}
    return {"item": item}


@app.put("/item/{item_id}")
async def item_update(item_id: int, item: Item):
    items[item_id - 1] = item
    return {"item": item}
