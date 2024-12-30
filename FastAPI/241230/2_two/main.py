from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/one/{hello}")
def one(hello: int):
    return hello + hello


@app.get("/two/{world}")
def two(world: str):
    return world + world


@app.get("/three/{author}/{count}")
def three(author: str, count: int):
    data = [
        {"author": "hojun", "title": "hello world 1"},
        {"author": "hojun", "title": "hello world 2"},
        {"author": "hojun", "title": "hello world 3"},
        {"author": "hojun", "title": "hello world 4"},
        {"author": "hojun", "title": "hello world 5"},
        {"author": "junho", "title": "hello world 6"},
        {"author": "junho", "title": "hello world 7"},
        {"author": "junho", "title": "hello world 8"},
        {"author": "junho", "title": "hello world 9"},
        {"author": "junho", "title": "hello world 10"},
    ]
    return list(filter(lambda x: x["author"] == author, data))[:count]


@app.get("/calculate/{operation}/{a}/{b}")
def calculate(operation: str, a: int, b: int):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Invalid operation"
