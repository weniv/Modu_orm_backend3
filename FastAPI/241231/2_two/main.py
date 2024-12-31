from fastapi import FastAPI

app = FastAPI(
    title="라이켓의 블로그 프로젝트",
    description="이 프로젝트는 대단한 프로젝트입니다.",
    version="1000.5.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/", tags=["items"])
async def read_items():
    """
    Retrieve items.

    This will use caching for faster responses.
    """
    return [{"item_id": "Foo"}]


@app.get("/items/1", tags=["items"])
async def read_items():
    """
    Retrieve items.

    This will use caching for faster responses.
    """
    return [{"item_id": "Foo"}]


@app.get("/items/2", tags=["items"])
async def read_items():
    """
    Retrieve items.

    This will use caching for faster responses.
    """
    return [{"item_id": "Foo"}]
